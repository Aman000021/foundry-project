"""Environment variables passed to the Hosted Agent container at registration.

Why this module exists
----------------------
``HostedAgentDefinition(environment_variables=...)`` is the only channel through
which configuration reaches a Hosted Agent container. Registering with an empty
mapping produces a container with no observability configuration at all:

* no ``OTEL_RESOURCE_ATTRIBUTES``: the enterprise resource model is not met,
  and telemetry cannot be attributed to a service, environment, or domain;
* no content-capture variables: Azure AI Agent Server defaults
  ``OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`` to ``"true"``, so
  prompts, completions, and tool results are captured and exported;
* no workflow identity: workflow spans fall back to the workflow name.

The container starts and answers requests, so the omission is not visible
without inspecting telemetry.

This module collects static variables from the deployment environment and
validates that the required ones are present before registration proceeds.
Deployment-derived values, such as ``NESTLE_AGENT_WORKFLOW_NAME``,
``NESTLE_OTEL_WORKFLOW_ID``, ``ai.app.id``, and ``deployment.id``, are added by
``register_agent.py`` after this static validation.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Final, Mapping


# Static variables that must be supplied through .env.deploy. Variables derived
# by register_agent.py must not be listed here because require_complete() runs
# before those values are injected.
REQUIRED_VARS: Final[tuple[str, ...]] = (
    "OTEL_RESOURCE_ATTRIBUTES",
    "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT",
    "ENABLE_SENSITIVE_DATA",
    "ENABLE_MESSAGE_EVENTS",
)


# Static variables passed through when present.
OPTIONAL_VARS: Final[tuple[str, ...]] = (
    # Model access
    "NESTLE_MODEL_ENDPOINT",
    "NESTLE_MODEL_DEPLOYMENT",
    "NESTLE_MODEL_TOKEN_SCOPE",
    "NESTLE_MODEL_TIMEOUT_SECONDS",

    # Nestle workflow identity/configuration. NESTLE_OTEL_WORKFLOW_ID may still
    # be accepted for compatibility, but register_agent.py overwrites it with a
    # value derived from AGENT_NAME before registration.
    "NESTLE_OTEL_WORKFLOW_ID",
    "NESTLE_OTEL_WORKFLOW_VERSION",
    "NESTLE_OTEL_DEFAULT_TRIGGER_TYPE",

    # Platform switches
    "NESTLE_OTEL_WORKFLOW_SPANS_ENABLED",
    "NESTLE_OTEL_SHUTDOWN_TIMEOUT_SECONDS",
    "NESTLE_OTEL_STRICT_ATTRIBUTES",
    "NESTLE_STARTUP_DIAGNOSTICS_ENABLED",
    "NESTLE_LOG_LEVEL",

    # Direct enterprise OTLP trace forwarding
    "NESTLE_OTEL_EXPORTER_OTLP_ENABLED",
    "NESTLE_OTEL_EXPORTER_OTLP_ENDPOINT",
    "NESTLE_OTEL_EXPORTER_OTLP_INSECURE",
    "NESTLE_OTEL_EXPORTER_OTLP_TIMEOUT_SECONDS",
    "NESTLE_OTEL_EXPORTER_OTLP_MODE",
)


# Resource attributes mandated by the enterprise model. service.name is
# excluded because the hosted runtime owns it and discards a supplied value.
REQUIRED_RESOURCE_KEYS: Final[tuple[str, ...]] = (
    "service.namespace",
    "service.version",
    "deployment.environment.name",
    "telemetry.schema.version",
    "domain.name",
)


class EnvironmentError_(ValueError):
    """Raised when the deployment environment is incomplete or invalid."""


@dataclass(frozen=True)
class EnvironmentPlan:
    """Variables resolved for the container, plus any problems found."""

    variables: dict[str, str] = field(default_factory=dict)
    missing: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.missing

    def describe(self) -> str:
        lines = [f"Container environment ({len(self.variables)} variable(s)):"]
        for key in sorted(self.variables):
            lines.append(f"  {key}={_redact(key, self.variables[key])}")
        for warning in self.warnings:
            lines.append(f"  WARNING: {warning}")
        for name in self.missing:
            lines.append(f"  MISSING: {name}")
        return "\n".join(lines)


def _redact(key: str, value: str) -> str:
    """Abbreviate long values; no secret is expected in this set."""
    del key
    if len(value) <= 90:
        return value
    return f"{value[:87]}..."


def _parse_resource_attributes(value: str) -> dict[str, str]:
    """Parse a comma-separated OTEL_RESOURCE_ATTRIBUTES value."""
    parsed: dict[str, str] = {}
    for entry in value.split(","):
        name, separator, raw = entry.partition("=")
        if separator and name.strip() and raw.strip():
            parsed[name.strip()] = raw.strip()
    return parsed


def build_environment(
    source: Mapping[str, str] | None = None,
) -> EnvironmentPlan:
    """Collect static container environment variables from *source*.

    This function does not raise. Inspect ``EnvironmentPlan.ok`` and call
    ``require_complete`` when registration should be blocked.
    """
    env = source if source is not None else os.environ
    variables: dict[str, str] = {}
    missing: list[str] = []
    warnings: list[str] = []

    for name in REQUIRED_VARS:
        value = (env.get(name) or "").strip()
        if value:
            variables[name] = value
        else:
            missing.append(name)

    for name in OPTIONAL_VARS:
        value = (env.get(name) or "").strip()
        if value:
            variables[name] = value

    resource_raw = variables.get("OTEL_RESOURCE_ATTRIBUTES", "")
    if resource_raw:
        attributes = _parse_resource_attributes(resource_raw)
        absent = [
            key for key in REQUIRED_RESOURCE_KEYS
            if key not in attributes
        ]
        if absent:
            warnings.append(
                "OTEL_RESOURCE_ATTRIBUTES is missing enterprise-required "
                f"attribute(s): {', '.join(absent)}"
            )
        if "service.name" in attributes:
            warnings.append(
                "OTEL_RESOURCE_ATTRIBUTES sets service.name, which the hosted "
                "runtime owns; the supplied value will be discarded"
            )

    capture = variables.get(
        "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT",
        "",
    )
    if capture.lower() not in ("false", "0"):
        warnings.append(
            "content capture is ENABLED; prompts, completions and tool results "
            "will be exported to Application Insights"
        )

    if "NESTLE_MODEL_DEPLOYMENT" not in variables:
        warnings.append(
            "NESTLE_MODEL_DEPLOYMENT is not set; the agent will run in echo mode"
        )

    return EnvironmentPlan(
        variables=variables,
        missing=tuple(missing),
        warnings=tuple(warnings),
    )


def require_complete(plan: EnvironmentPlan) -> dict[str, str]:
    """Return a copy of the variables, raising when a required one is absent."""
    if not plan.ok:
        raise EnvironmentError_(
            "Missing required environment variable(s): "
            + ", ".join(plan.missing)
            + ". Registering without these produces a container with no "
            "observability configuration and content capture enabled."
        )
    return dict(plan.variables)


def with_resource_attributes(
    variables: Mapping[str, str],
    extra: Mapping[str, str],
) -> dict[str, str]:
    """Return a copy with *extra* merged into OTEL_RESOURCE_ATTRIBUTES.

    Deployment-time values, such as ``deployment.id`` and ``ai.app.id``,
    override any static value with the same key. Keys and values must not
    contain commas or equals signs.
    """
    result = dict(variables)
    attrs = _parse_resource_attributes(
        result.get("OTEL_RESOURCE_ATTRIBUTES", "")
    )

    for key, value in extra.items():
        normalized_key = str(key).strip()
        normalized_value = str(value).strip()

        if not normalized_key or not normalized_value:
            raise EnvironmentError_(
                f"resource attribute key and value must not be empty: {key}"
            )
        if any(char in normalized_key for char in ",="):
            raise EnvironmentError_(
                f"invalid resource attribute key: {normalized_key}"
            )
        if any(char in normalized_value for char in ",="):
            raise EnvironmentError_(
                f"invalid resource attribute value for: {normalized_key}"
            )

        attrs[normalized_key] = normalized_value

    result["OTEL_RESOURCE_ATTRIBUTES"] = ",".join(
        f"{key}={value}" for key, value in attrs.items()
    )
    return result


__all__ = [
    "REQUIRED_VARS",
    "OPTIONAL_VARS",
    "REQUIRED_RESOURCE_KEYS",
    "EnvironmentPlan",
    "EnvironmentError_",
    "build_environment",
    "require_complete",
    "with_resource_attributes",
]
