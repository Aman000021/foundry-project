# Minimal Microsoft Foundry Hosted Agent Baseline

This experiment establishes the smallest working container-based Microsoft Foundry Hosted Agent baseline. It separates the shared runtime, the agent implementation, and the deployment utility so each layer can evolve independently.

The baseline intentionally does not call an LLM and does not add custom observability. Its purpose is to prove the complete hosting path before further capabilities are introduced.

## Scope

The implementation contains three parts:

1. **Golden image**: shared Python and Foundry Hosted Agent runtime.
2. **Hosted Agent image**: minimal solution code that returns a deterministic response.
3. **Deployment utility**: registers a container-image Hosted Agent version in a Foundry project and waits for activation.

The validated image relationship is:

```text
base/python:3.13-slim
└── hosted-agent:dev-init
    └── hosted-agent-dev-01:init-v1
```

- `hosted-agent:dev-init` is the reusable golden image.
- `hosted-agent-dev-01:init-v1` is the deployable agent image.
- `hosted-agent-init` is the Foundry Agent name.

## Prerequisites

- Docker
- Access to the approved Azure Container Registry
- Azure CLI authentication for the target tenant
- Permission to create Hosted Agent versions in the target Foundry project
- A local Python virtual environment for the deployment utility

Do not commit `.env.deploy` or environment-specific identifiers into a reusable template.

---

# 1. Golden image

## Purpose

The golden image provides the common runtime required by every derived Hosted Agent:

- Python 3.13
- Microsoft Foundry Responses Agent Server runtime
- Generic wrapper entry point
- Dynamic loading of solution code
- Startup network diagnostics
- Non-root container execution

The golden image does not contain solution-specific agent code, LLM calls, A2A logic, or custom observability code.

## Golden-image files

```text
golden-image/
├── Dockerfile
├── requirements.txt
└── src/
    ├── __init__.py
    ├── diagnostics.py
    ├── entrypoint.py
    └── main.py
```

## `requirements.txt`

```text
azure-ai-agentserver-responses==2.1.0
```

`azure-ai-agentserver-responses` supplies `ResponsesAgentServerHost`, `TextResponse`, and the Responses protocol implementation. Its dependencies include the Agent Server Core runtime.

## Golden-image `Dockerfile`

```dockerfile
FROM glbldvplatform644acr.azurecr.io/base/python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8088

WORKDIR /app

RUN groupadd \
        --system \
        --gid 10001 \
        agent \
    && useradd \
        --system \
        --uid 10001 \
        --gid agent \
        --home-dir /nonexistent \
        --no-create-home \
        --shell /usr/sbin/nologin \
        agent

COPY requirements.txt .

RUN python -m pip install \
    --no-cache-dir \
    --requirement requirements.txt

COPY --chown=root:root ./src ./src

USER 10001:10001

EXPOSE 8088

CMD ["python", "-m", "src.main"]
```

## Wrapper flow

At container startup:

1. `src.main` reads `AGENT_MODULE` and `AGENT_ENTRYPOINT`.
2. `src.entrypoint` imports the configured solution module dynamically.
3. `src.diagnostics` checks DNS, TCP 443, TLS, and basic HTTPS reachability for the platform-provided Foundry project endpoint.
4. The resolved solution entry point is called.
5. The solution starts `ResponsesAgentServerHost`.

The platform reserves `FOUNDRY_*` and `AGENT_*` deployment variables. Platform-owned variables must not be passed through `HostedAgentDefinition.environment_variables`.

## Build and push the golden image

From the golden-image directory:

```bash
docker build \
  -t glbldvplatform644acr.azurecr.io/hosted-agent:dev-init \
  .
```

```bash
docker push \
  glbldvplatform644acr.azurecr.io/hosted-agent:dev-init
```

---

# 2. Minimal Hosted Agent

## Purpose

The derived agent proves that:

- the golden-image wrapper can load team code;
- `ResponsesAgentServerHost` starts correctly;
- the Responses endpoint invokes the registered handler;
- `TextResponse` reaches the caller;
- no model or external service is required for the baseline test.

## Hosted Agent files

```text
hosted-agent/
├── .dockerignore
├── Dockerfile
└── src/
    ├── __init__.py
    └── hosted_agent.py
```

The Hosted Agent image does not need a solution `requirements.txt` because its only external runtime dependency is already supplied by the golden image.

## `src/hosted_agent.py`

```python
"""Minimal Microsoft Foundry Hosted Agent validation implementation."""

import logging
from typing import Any

from azure.ai.agentserver.responses import (
    InMemoryResponseProvider,
    ResponsesAgentServerHost,
    TextResponse,
)

logger = logging.getLogger(__name__)

app = ResponsesAgentServerHost(
    store=InMemoryResponseProvider(),
)


def extract_user_text(request: Any) -> str:
    """Extract textual input from the supported request representation."""
    request_input = getattr(request, "input", None)

    if request_input is None:
        return ""

    if isinstance(request_input, str):
        return request_input.strip()

    return str(request_input).strip()


@app.response_handler
async def handle_response(
    request: Any,
    context: Any,
    cancellation_signal: Any,
) -> TextResponse:
    """Return a deterministic response for runtime validation."""
    del cancellation_signal

    user_text = extract_user_text(request)

    logger.info(
        "Hosted Agent request received: input_present=%s",
        bool(user_text),
    )

    if not user_text:
        return TextResponse(
            context=context,
            request=request,
            text="No textual input was provided.",
        )

    return TextResponse(
        context=context,
        request=request,
        text=f"Hosted Agent is running. Received: {user_text}",
    )


def main() -> None:
    """Start the Foundry Responses host."""
    app.run()
```

## Hosted Agent `Dockerfile`

```dockerfile
ARG BASE_REGISTRY=glbldvplatform644acr.azurecr.io
FROM ${BASE_REGISTRY}/hosted-agent:dev-init

COPY --chown=root:root ./src ./src

ENV AGENT_MODULE=src.hosted_agent \
    AGENT_ENTRYPOINT=main
```

`AGENT_MODULE` and `AGENT_ENTRYPOINT` are image-level wrapper settings. They identify which module and callable the golden-image wrapper must launch.

## Build and push the Hosted Agent image

From the Hosted Agent directory:

```bash
docker build \
  -t glbldvplatform644acr.azurecr.io/hosted-agent-dev-01:init-v1 \
  .
```

```bash
docker push \
  glbldvplatform644acr.azurecr.io/hosted-agent-dev-01:init-v1
```

Do not deploy `hosted-agent:dev-init` directly. That image contains the shared runtime but not the derived agent configuration and solution module.

---

# 3. Deployment utility

## Purpose

The deployment utility:

1. Loads deployment configuration from `.env.deploy`.
2. Authenticates with `DefaultAzureCredential`.
3. constructs the full ACR image reference.
4. creates a new container-based Hosted Agent version;
5. declares the Responses protocol version;
6. polls the version until it becomes active, fails, or reaches the polling limit.

The deployment utility is local tooling. Its dependencies do not belong in the golden image.

## Deployment files

```text
deploy/
├── .env.deploy
├── register_agent.py
└── requirements.txt
```

## Deployment `requirements.txt`

```text
azure-ai-projects>=2.6,<3
azure-identity
python-dotenv
```

For full reproducibility, replace ranges and unpinned packages with the exact versions validated by the experiment before promotion to a reusable template.

## `.env.deploy`

Use plain values, without HTML link markup:

```dotenv
FOUNDRY_PROJECT_ENDPOINT=<foundry-project-endpoint>
AGENT_NAME=hosted-agent-init
ACR_LOGIN_SERVER=glbldvplatform644acr.azurecr.io
AGENT_IMAGE=hosted-agent-dev-01:init-v1
AGENT_CPU=1
AGENT_MEMORY=2Gi
AGENT_PROTOCOL_VERSION=1.0.0
```

`FOUNDRY_PROJECT_ENDPOINT` is used locally to create `AIProjectClient`. It must not be added to `HostedAgentDefinition.environment_variables`, because `FOUNDRY_*` and `AGENT_*` names are reserved for platform use.

The minimal `HostedAgentDefinition` must not inject custom environment variables:

```python
definition = HostedAgentDefinition(
    cpu=cpu,
    memory=memory,
    container_configuration=ContainerConfiguration(
        image=full_image,
    ),
    protocol_versions=[
        ProtocolVersionRecord(
            protocol=AgentEndpointProtocol.RESPONSES,
            version=protocol_version,
        ),
    ],
)
```

## Create the deployment virtual environment

From the deployment directory:

```bash
python3 -m venv .vDeploy
```

```bash
.vDeploy/bin/python -m pip install \
  --requirement requirements.txt
```

## Authenticate

Use the approved Azure authentication procedure for the target environment. `DefaultAzureCredential` uses the available supported local credential.

## Register the agent

From the deployment directory:

```bash
.vDeploy/bin/python register_agent.py
```

A successful run creates a new version of `hosted-agent-init` and reports that the Hosted Agent is active.

---

# End-to-end validation

## 1. Deployment validation

Confirm that `register_agent.py` reports:

```text
Hosted Agent is active.
```

This proves that Foundry can retrieve the derived image and start the Hosted Agent container.

## 2. Runtime validation

Open the deployed `hosted-agent-init` agent in the Foundry test interface and send:

```text
Hello
```

Expected response:

```text
Hosted Agent is running. Received: Hello
```

This proves the complete request path:

```text
Foundry Responses endpoint
→ Agent Server Responses runtime
→ golden-image wrapper
→ src.hosted_agent.main
→ handle_response
→ TextResponse
→ caller
```

## 3. Log validation

Confirm that the container logs do not report:

```text
AGENT_MODULE environment variable is not set
```

If that message appears, verify that:

- the deployment references `hosted-agent-dev-01:init-v1` rather than `hosted-agent:dev-init`;
- the derived image was rebuilt and pushed;
- the derived Dockerfile defines `AGENT_MODULE=src.hosted_agent` and `AGENT_ENTRYPOINT=main`.

## Built-in telemetry observation

The Agent Server Core runtime may initialize platform-provided telemetry automatically. During this baseline validation, telemetry export returned `Forbidden` because the Hosted Agent identity did not have permission to publish to the configured monitoring resource.

This baseline does not add or configure custom observability. Telemetry authorization, destination ownership, exporter behavior, and observability extensions are explicitly deferred to the next experiment phase.

---

# Baseline completion criteria

The minimal baseline can be closed when all items below are true:

- [x] Golden image builds and is available as `hosted-agent:dev-init`.
- [x] Derived Hosted Agent image builds and is available as `hosted-agent-dev-01:init-v1`.
- [x] Deployment utility creates an agent version from the derived image.
- [x] Hosted Agent version reaches the active state.
- [x] A Responses request invokes the agent and returns the expected deterministic text.
- [x] Final source tree contains no stale `__pycache__`, Presentation Agent, A2A, charting, or temporary files.
- [x] `.env.deploy` is excluded from Git and contains no committed environment-specific values.
- [x] The experiment issue is updated with the final validation result and image references.

---

# Next phase: observability experiment

After the baseline completion criteria are satisfied, copy this known-good implementation into the observability experiment folder and evolve that copy.

The observability phase should begin from the confirmed facts established here:

- the golden-image wrapper loads derived solution code correctly;
- the Responses Agent Server runtime starts correctly;
- the derived agent can be registered and activated;
- the baseline requires no LLM, A2A, or solution-specific dependency;
- Agent Server Core already has built-in telemetry behavior that must be understood before adding custom instrumentation.

Keep this baseline unchanged so it remains the control implementation for comparison with each observability change.
