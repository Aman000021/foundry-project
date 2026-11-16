"""Telemetry for Hosted Agent deployment tooling.

Unlike agenthost.observability, this process runs outside the hosted runtime,
so it OWNS its TracerProvider and LoggerProvider.

Rules:
* Fail-open: telemetry problems never fail a deployment.
* Resource is built explicitly; OTEL_RESOURCE_ATTRIBUTES in the process
  environment belongs to the agent container and is ignored.
* Only DEPLOY_* variables are read.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any, Final

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

SCOPE: Final = "nestle.agentic.deployment"
SCOPE_VERSION: Final = "1.0.0"
DEPLOY_LOGGER: Final = "hosted_agent_deploy"

_TRUE: Final = frozenset({"1", "true", "yes", "on"})
log = logging.getLogger(DEPLOY_LOGGER)


def _flag(name: str, default: bool) -> bool:
    raw = (os.environ.get(name) or "").strip().lower()
    return default if not raw else raw in _TRUE


def _text(name: str, default: str = "") -> str:
    return (os.environ.get(name) or default).strip()


@dataclass
class DeployTelemetry:
    tracer: Any
    tracer_provider: TracerProvider | None = None
    logger_provider: LoggerProvider | None = None
    destinations: tuple[str, ...] = field(default_factory=tuple)

    def shutdown(self, timeout_millis: int = 10_000) -> None:
        """Flush and close. Never raises."""
        for provider in (self.tracer_provider, self.logger_provider):
            if provider is None:
                continue
            try:
                provider.force_flush(timeout_millis)
                provider.shutdown()
            except Exception:  # pragma: no cover
                pass


def _resource() -> Resource:
    attrs = {
        "service.name": "foundry-hosted-agent-deployer",
        "service.namespace": "nestle-ai-agents",
        "service.version": _text("DEPLOY_TOOL_VERSION", "1.0.0"),
        "deployment.environment.name": _text("DEPLOY_ENVIRONMENT", "dev"),
        "telemetry.schema.version": "1.0.0",
        "domain.name": "ai-services",
        "owner.team": "adi-foundry",
        "data.classification": "internal",
        "telemetry.sdk.language": "python",
        "telemetry.sdk.name": "opentelemetry",
    }
    run_id = _text("GITHUB_RUN_ID")  # empty locally
    attrs["service.instance.id"] = f"gh-{run_id}" if run_id else "local"
    if run_id:
        attrs["cicd.pipeline.run.id"] = run_id
    return Resource(attrs)  # NOT Resource.create(): ignore agent env


def _attach_otlp(tp: TracerProvider, lp: LoggerProvider) -> str | None:
    endpoint = _text("DEPLOY_OTEL_OTLP_ENDPOINT")
    if not endpoint:
        return None
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

    insecure = _flag("DEPLOY_OTEL_OTLP_INSECURE", False)
    tp.add_span_processor(BatchSpanProcessor(
        OTLPSpanExporter(endpoint=endpoint, insecure=insecure, timeout=10)))
    if _flag("DEPLOY_OTEL_OTLP_LOGS_ENABLED", False):
        from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
        lp.add_log_record_processor(BatchLogRecordProcessor(
            OTLPLogExporter(endpoint=endpoint, insecure=insecure, timeout=10)))
    return f"otlp:{endpoint}"


def _attach_azure_monitor(tp: TracerProvider, lp: LoggerProvider) -> str | None:
    conn = _text("DEPLOY_APPLICATIONINSIGHTS_CONNECTION_STRING")
    if not conn:
        return None
    from azure.monitor.opentelemetry.exporter import (
        AzureMonitorLogExporter,
        AzureMonitorTraceExporter,
    )

    kwargs: dict[str, Any] = {"connection_string": conn}
    if _flag("DEPLOY_APPLICATIONINSIGHTS_AAD_AUTH", True):
        from azure.identity import DefaultAzureCredential
        kwargs["credential"] = DefaultAzureCredential()
    tp.add_span_processor(BatchSpanProcessor(AzureMonitorTraceExporter(**kwargs)))
    lp.add_log_record_processor(BatchLogRecordProcessor(AzureMonitorLogExporter(**kwargs)))
    return "azure-monitor"

class _StripCodePath(logging.Filter):
    """Keep only the file name in exported log records (no local paths)."""
    def filter(self, record: logging.LogRecord) -> bool:
        record.pathname = record.filename
        return True

def init_deploy_telemetry() -> DeployTelemetry:
    """Initialise deploy telemetry. Call AFTER load_dotenv. Never raises."""
    if not _flag("DEPLOY_OTEL_ENABLED", True):
        return DeployTelemetry(trace.NoOpTracer())
    try:
        resource = _resource()
        tp = TracerProvider(resource=resource)
        lp = LoggerProvider(resource=resource)
        destinations: list[str] = []
        for attach in (_attach_otlp, _attach_azure_monitor):
            try:
                dest = attach(tp, lp)
                if dest:
                    destinations.append(dest)
            except Exception as exc:
                log.warning("deploy telemetry: %s failed: %s: %s",
                            attach.__name__, type(exc).__name__, exc)
        if not destinations:
            log.warning("deploy telemetry: no destination configured; disabled")
            return DeployTelemetry(trace.NoOpTracer())

        trace.set_tracer_provider(tp)   # we own this process
        set_logger_provider(lp)
        # Bridge only our logger, not root: avoids exporting azure SDK noise
        # and exporter self-logging feedback loops.
        handler = LoggingHandler(level=logging.INFO, logger_provider=lp)
        handler.addFilter(_StripCodePath())
        logging.getLogger(DEPLOY_LOGGER).addHandler(handler)
        return DeployTelemetry(tp.get_tracer(SCOPE, SCOPE_VERSION), tp, lp,
                               tuple(destinations))
    except Exception as exc:  # pragma: no cover
        log.warning("deploy telemetry init failed: %s: %s", type(exc).__name__, exc)
        return DeployTelemetry(trace.NoOpTracer())


__all__ = ["DEPLOY_LOGGER", "DeployTelemetry", "init_deploy_telemetry"]