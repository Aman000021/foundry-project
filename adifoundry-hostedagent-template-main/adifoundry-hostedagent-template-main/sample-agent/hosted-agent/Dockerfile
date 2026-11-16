# Example agent image built on the Nestle golden image.
#
# Changes from the previous pattern:
#
#  * No CMD. The golden image already runs `python -m agenthost.main`; an agent
#    image that sets its own CMD bypasses observability initialisation and
#    startup diagnostics.
#
#  * Platform code lives in /app/agenthost, not /app/src, so copying solution
#    code into /app/src can no longer shadow a platform module. Previously both
#    occupied `src`, and an agent file named main.py or diagnostics.py would
#    silently replace the platform's.
#
#  * requirements.txt is installed with the golden image's constraints so a
#    solution dependency cannot pull an incompatible OpenTelemetry version into
#    the image and break the Microsoft instrumentation.

ARG BASE_REGISTRY=glbldvplatform644acr.azurecr.io
ARG GOLDEN_IMAGE=incubator/hosted-agent:dev-cribl-v2

FROM ${BASE_REGISTRY}/${GOLDEN_IMAGE}

USER root

# Agent dependencies, constrained by the versions the golden image resolved.
COPY requirements.txt /app/agent-requirements.txt
RUN PIP_USER=0 python -m pip install \
        --no-cache-dir \
        -c /app/constraints.txt \
        -r /app/agent-requirements.txt

# Solution code. Isolated from platform code by directory.
COPY --chown=root:root ./src /app/src

USER 10001:10001

# --------------------------------------------------------------------------
# Agent identity
# --------------------------------------------------------------------------
ENV AGENT_MODULE=src.hosted_agent \
    AGENT_ENTRYPOINT=main

# --------------------------------------------------------------------------
# Observability -- declared per environment, not baked into the image
# --------------------------------------------------------------------------
# These belong in the deployment manifest, not here. They are shown as a
# reference for the full set a deployment must provide.
#
# Solution identity, merged into the Microsoft-owned Resource:
#   OTEL_RESOURCE_ATTRIBUTES="service.namespace=nestle-ai-agents,\
#     service.version=1.0.0,deployment.environment.name=dev,\
#     telemetry.schema.version=1.0.0,domain.name=ai-services,\
#     ai.app.id=invoice-agent,owner.team=adi-foundry,\
#     data.classification=confidential"
#
# Workflow identity for Nestle workflow spans:
#   NESTLE_OTEL_WORKFLOW_ID=invoice-wf
#   NESTLE_OTEL_WORKFLOW_VERSION=1.0.0
#   NESTLE_OTEL_DEFAULT_TRIGGER_TYPE=a2a
#
# Content capture -- all three must be declared explicitly. Unset means ON.
#   OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=false
#   ENABLE_SENSITIVE_DATA=false
#   ENABLE_MESSAGE_EVENTS=false
