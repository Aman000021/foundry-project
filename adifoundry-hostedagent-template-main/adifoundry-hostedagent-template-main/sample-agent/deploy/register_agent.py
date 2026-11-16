"""Register the minimal container-based Microsoft Foundry Hosted Agent."""
import json
import logging
import os
import sys
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentEndpointProtocol,
    ContainerConfiguration,
    HostedAgentDefinition,
    ProtocolVersionRecord,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from opentelemetry.trace import Span, Status, StatusCode

#from agent_environment import build_environment, require_complete
from agent_environment import build_environment, require_complete, with_resource_attributes
from deploy_telemetry import DEPLOY_LOGGER, init_deploy_telemetry

log = logging.getLogger(DEPLOY_LOGGER)


def required_env(name: str) -> str:
    """Return a required deployment environment variable."""
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Required environment variable is missing: {name}"
        )
    return value


def optional_env(name: str, default: str) -> str:
    """Return an optional deployment environment variable."""
    return os.environ.get(name, default)

def parse_image_reference(agent_image: str) -> dict[str, str]:
    """Parse an agent image into repository, tag, and optional digest."""
    reference = agent_image.strip()

    if "@" in reference:
        repository, digest = reference.rsplit("@", 1)
        return {
            "repository": repository,
            "tag": "",
            "digest": digest,
        }

    last_segment = reference.rsplit("/", 1)[-1]
    if ":" in last_segment:
        repository, tag = reference.rsplit(":", 1)
        return {
            "repository": repository,
            "tag": tag,
            "digest": "",
        }

    return {
        "repository": reference,
        "tag": "",
        "digest": "",
    }

def serialize(value: Any) -> dict[str, Any]:
    """Convert an SDK response into a printable dictionary."""
    if hasattr(value, "as_dict"):
        return value.as_dict()
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if isinstance(value, dict):
        return value
    return vars(value)


def _console_logging() -> None:
    """Console output for the deploy logger only (no Azure SDK noise)."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    log.propagate = False


def _finish(root: Span, status: str, failed_at: str | None = None,
            message: str | None = None) -> None:
    """Record the workflow outcome on the root span."""
    root.set_attribute("workflow.status", status)
    if failed_at:
        root.set_attribute("workflow.failed_at", failed_at)
        root.set_status(Status(StatusCode.ERROR, message or status))
    else:
        root.set_status(Status(StatusCode.OK))


def deploy(tracer: Any, run_id: str) -> int:
    """Create a Hosted Agent version and wait for activation."""
    trigger = "pipeline" if os.environ.get("GITHUB_ACTIONS") == "true" else "local"

    with tracer.start_as_current_span(
        "workflow.deploy-hosted-agent",
        attributes={
            "run.id": run_id,
            "trigger.type": trigger,
            "deployment.environment.name": optional_env("DEPLOY_ENVIRONMENT", "dev"),
            "cicd.pipeline.run.id": os.environ.get("GITHUB_RUN_ID", ""),
        },
        record_exception=True,
        set_status_on_exception=True,
    ) as root:
        trace_id = f"{root.get_span_context().trace_id:032x}"

        # ---------------------------------------------------------------
        # step.validate_environment
        # ---------------------------------------------------------------
        with tracer.start_as_current_span("step.validate_environment") as step:
            endpoint = required_env("FOUNDRY_PROJECT_ENDPOINT")
            agent_name = required_env("AGENT_NAME")
            registry = required_env("ACR_LOGIN_SERVER")
            agent_image = required_env("AGENT_IMAGE")
            cpu = optional_env("AGENT_CPU", "1")
            memory = optional_env("AGENT_MEMORY", "2Gi")
            protocol_version = optional_env("AGENT_PROTOCOL_VERSION", "1.0.0")
            full_image = f"{registry.rstrip('/')}/{agent_image.lstrip('/')}"
            image_info = parse_image_reference(agent_image)

            root.set_attribute("gen_ai.agent.name", agent_name)
            # root.set_attribute("container.image.name", agent_image)
            root.set_attribute("container.image.reference", full_image)
            root.set_attribute("container.image.name", image_info["repository"])

            if image_info["tag"]:
                root.set_attribute("container.image.tag", image_info["tag"])

            if image_info["digest"]:
                root.set_attribute("container.image.digest", image_info["digest"])

            # Registering with an empty mapping produces a container with no
            # observability configuration and content capture enabled by
            # default, so this is validated before any call to Foundry.
            environment_plan = build_environment()

            log.info("Hosted Agent container-image deployment")
            log.info("---------------------------------------")
            log.info("Agent name       : %s", agent_name)
            log.info("Container image  : %s", full_image)
            log.info("CPU / Memory     : %s / %s", cpu, memory)
            log.info("Protocol         : responses %s", protocol_version)
            log.info("run.id           : %s", run_id)
            log.info("trace_id         : %s", trace_id)
            # Console only: describe() contains variable VALUES (endpoints, IPs).
            print()
            print(f"Project endpoint : {endpoint}")
            print(environment_plan.describe())
            print()

            container_environment = require_complete(environment_plan)

            container_environment["NESTLE_AGENT_WORKFLOW_NAME"] = agent_name
            container_environment["NESTLE_OTEL_WORKFLOW_ID"] = f"{agent_name}-wf"

            container_environment = with_resource_attributes(
                container_environment,
                {
                    "ai.app.id": agent_name,
                    "deployment.id": run_id,
                },
            )

            step.set_attribute("deployment.id", run_id)
            step.set_attribute(
                "environment.variable.count",
                len(container_environment),
            )
            step.set_attribute("agent.cpu", cpu)
            step.set_attribute("agent.memory", memory)
            step.set_attribute("agent.protocol.version", protocol_version)

        credential = DefaultAzureCredential()
        project = AIProjectClient(
            endpoint=endpoint,
            credential=credential,
            allow_preview=True,
        )
        try:
            # -----------------------------------------------------------
            # step.create_version
            # -----------------------------------------------------------
            with tracer.start_as_current_span("step.create_version") as step:
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
                    environment_variables=container_environment,
                )
                log.info("Creating Hosted Agent version...")
                created = project.agents.create_version(
                    agent_name=agent_name,
                    definition=definition,
                    description="Minimal Microsoft Foundry Hosted Agent",
                    metadata={
                        "DEPLOY_TIMESTAMP": datetime.now(UTC).isoformat(),
                        "DEPLOY_RUN_ID": run_id,
                        "DEPLOY_TRACE_ID": trace_id,
                        "AGENT_IMAGE_REFERENCE": full_image,
                        "AGENT_IMAGE_REPOSITORY": image_info["repository"],
                        "AGENT_IMAGE_TAG": image_info["tag"] or "none",
                        "AGENT_IMAGE_DIGEST": image_info["digest"] or "none",
                    },
                )
                version = (
                    created.get("version")
                    if isinstance(created, dict)
                    else getattr(created, "version", None)
                )
                if not version:
                    log.error("Agent version was created, but no version value was returned.")
                    print(json.dumps(serialize(created), indent=2, default=str))
                    step.set_status(Status(StatusCode.ERROR, "no version returned"))
                    _finish(root, "failed", "create_version", "no version returned")
                    return 1

                step.set_attribute("gen_ai.agent.version", str(version))
                root.set_attribute("gen_ai.agent.version", str(version))
                log.info("Created version: %s", version)

            # -----------------------------------------------------------
            # step.wait_for_active
            # -----------------------------------------------------------
            with tracer.start_as_current_span("step.wait_for_active") as step:
                log.info("Polling for status...")
                last_status: str | None = None
                for index in range(60):
                    agent_version = project.agents.get_version(
                        agent_name=agent_name,
                        agent_version=version,
                    )
                    if isinstance(agent_version, dict):
                        status = agent_version.get("status")
                        error = agent_version.get("error")
                    else:
                        status = getattr(agent_version, "status", None)
                        error = getattr(agent_version, "error", None)

                    #status_text = str(status).lower()
                    status_text = str(getattr(status, "value", status)).lower()                    
                    print(f"  {index:02d} status={status} error={error}")
                    if status_text != last_status:
                        step.add_event("status.changed", {"status": status_text, "poll": index})
                        last_status = status_text
                    step.set_attribute("poll.count", index + 1)
                    step.set_attribute("agent.final_status", status_text)

                    if status_text.endswith("active"):
                        log.info("Hosted Agent is active: %s version %s", agent_name, version)
                        _finish(root, "succeeded")
                        return 0

                    if status_text.endswith("failed"):
                        log.error("Provisioning failed: %s version %s error=%s",
                                  agent_name, version, error)
                        print(json.dumps(serialize(agent_version), indent=2, default=str))
                        step.set_status(Status(StatusCode.ERROR, "provisioning failed"))
                        _finish(root, "failed", "wait_for_active", "provisioning failed")
                        return 1

                    time.sleep(5)

                log.error("Timed out waiting for active status: %s version %s",
                          agent_name, version)
                step.set_status(Status(StatusCode.ERROR, "timeout"))
                _finish(root, "timeout", "wait_for_active", "timeout")
                return 2
        finally:
            project_close = getattr(project, "close", None)
            if callable(project_close):
                project_close()
            credential_close = getattr(credential, "close", None)
            if callable(credential_close):
                credential_close()


def main() -> int:
    load_dotenv(Path(__file__).resolve().parent / ".env.deploy", override=True)
    _console_logging()
    telemetry = init_deploy_telemetry()
    run_id = str(uuid.uuid4())
    try:
        return deploy(telemetry.tracer, run_id)
    except Exception as exc:
        # Root span already recorded the exception; keep console output useful.
        log.error("Deployment failed: %s: %s", type(exc).__name__, exc)
        return 1
    finally:
        telemetry.shutdown()


if __name__ == "__main__":
    sys.exit(main())
