"""Azure AI Foundry model client for the hosted agent.

Builds an OpenAI-compatible client pointed at the Foundry project's ``/openai/v1``
surface, authenticated with the agent's managed identity.

Why the plain OpenAI SDK
------------------------
``microsoft-opentelemetry`` -- a hard dependency of the Agent Server -- ships
``opentelemetry-instrumentation-openai-v2`` and enables it automatically, so
calls made through this client emit Microsoft GenAI ``chat`` spans with no
instrumentation code here.

That auto-enable is conditional. ``_disable_openai_v2_instrumentation`` turns
the OpenAI instrumentor **off** when ``agent_framework`` or ``langchain_core``
is importable, because those ship instrumentors of their own that would emit the
same spans. Installing either package into this agent therefore silently changes
which component produces the ``chat`` span.

Authentication
--------------
A bearer token is attached per request rather than held on the client, so token
refresh is handled by the credential and no shared mutable state is touched by
concurrent requests. ``get_bearer_token_provider`` caches and refreshes
internally, so calling it per request is cheap.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any, Final

logger = logging.getLogger(__name__)

#: Foundry project endpoint, injected into the container by the platform.
#:
#: ``FOUNDRY_*`` and ``AGENT_*`` are reserved by the container-image-spec and
#: are rejected if supplied in the registration payload, so this value cannot
#: be set by the deployment -- it is read as the platform provides it.
PLATFORM_ENDPOINT_VAR: Final = "FOUNDRY_PROJECT_ENDPOINT"

#: Optional override, used when the platform does not inject an endpoint.
#: Deployment-supplied variables must avoid the reserved prefixes.
ENDPOINT_OVERRIDE_VAR: Final = "NESTLE_MODEL_ENDPOINT"

#: Deployment name of the model to call.
MODEL_DEPLOYMENT_VAR: Final = "NESTLE_MODEL_DEPLOYMENT"
#: Entra scope requested for the model call.
TOKEN_SCOPE_VAR: Final = "NESTLE_MODEL_TOKEN_SCOPE"
#: Request timeout in seconds.
TIMEOUT_VAR: Final = "NESTLE_MODEL_TIMEOUT_SECONDS"

#: Path appended to the project endpoint to reach the OpenAI-compatible surface.
#: Matches the path probed by the golden image's startup diagnostics.
OPENAI_V1_SUFFIX: Final = "/openai/v1"

DEFAULT_TOKEN_SCOPE: Final = "https://ai.azure.com/.default"
DEFAULT_TIMEOUT_SECONDS: Final = 60.0

#: The OpenAI SDK requires a non-empty api_key. The real credential is supplied
#: per request as an Authorization header, so this value is never used.
_PLACEHOLDER_KEY: Final = "managed-identity"


class ModelUnavailable(RuntimeError):
    """Raised when the model client cannot be constructed."""


@dataclass(frozen=True)
class ModelConfig:
    """Resolved model configuration."""

    endpoint: str
    deployment: str
    token_scope: str
    timeout_seconds: float

    @property
    def base_url(self) -> str:
        return f"{self.endpoint.rstrip('/')}{OPENAI_V1_SUFFIX}"

    @classmethod
    def from_environment(cls) -> "ModelConfig | None":
        """Build configuration, or return ``None`` when the model is not configured.

        Returning ``None`` rather than raising lets the agent run in a
        deterministic echo mode, which is useful for validating the runtime and
        the telemetry path before a model is wired up.
        """
        # Prefer an explicit override; otherwise use the endpoint the platform
        # injects. The override exists because the platform variable cannot be
        # supplied at registration time.
        endpoint = (
            (os.environ.get(ENDPOINT_OVERRIDE_VAR) or "").strip()
            or (os.environ.get(PLATFORM_ENDPOINT_VAR) or "").strip()
        )
        deployment = (os.environ.get(MODEL_DEPLOYMENT_VAR) or "").strip()
        if not endpoint or not deployment:
            missing = [
                name
                for name, value in (
                    (f"{PLATFORM_ENDPOINT_VAR} or {ENDPOINT_OVERRIDE_VAR}", endpoint),
                    (MODEL_DEPLOYMENT_VAR, deployment),
                )
                if not value
            ]
            logger.info(
                "Model not configured (%s unset); agent will run in echo mode",
                ", ".join(missing),
            )
            return None

        raw_timeout = (os.environ.get(TIMEOUT_VAR) or "").strip()
        try:
            timeout = float(raw_timeout) if raw_timeout else DEFAULT_TIMEOUT_SECONDS
        except ValueError:
            logger.warning(
                "%s=%r is not a number; using %.1f",
                TIMEOUT_VAR,
                raw_timeout,
                DEFAULT_TIMEOUT_SECONDS,
            )
            timeout = DEFAULT_TIMEOUT_SECONDS

        return cls(
            endpoint=endpoint,
            deployment=deployment,
            token_scope=(os.environ.get(TOKEN_SCOPE_VAR) or DEFAULT_TOKEN_SCOPE).strip(),
            timeout_seconds=timeout,
        )


class ModelClient:
    """Lazily constructed OpenAI-compatible client for a Foundry deployment.

    Construction is deferred to first use so that an authentication or import
    problem surfaces as a failed request rather than a container that will not
    start.
    """

    __slots__ = ("_config", "_client", "_token_provider", "_credential", "_failed")

    def __init__(self, config: ModelConfig) -> None:
        self._config = config
        self._client: Any = None
        self._token_provider: Any = None
        self._credential: Any = None
        self._failed: str | None = None

    @property
    def config(self) -> ModelConfig:
        return self._config

    @property
    def deployment(self) -> str:
        return self._config.deployment

    def _ensure(self) -> None:
        if self._client is not None:
            return
        if self._failed is not None:
            raise ModelUnavailable(self._failed)

        try:
            from azure.identity import (  # noqa: PLC0415
                DefaultAzureCredential,
                get_bearer_token_provider,
            )
            from openai import AsyncOpenAI  # noqa: PLC0415
        except ImportError as exc:
            self._failed = (
                f"model dependencies are not installed: {exc}. "
                "Add 'openai' and 'azure-identity' to requirements.txt."
            )
            raise ModelUnavailable(self._failed) from exc

        try:
            self._credential = DefaultAzureCredential()
            self._token_provider = get_bearer_token_provider(
                self._credential, self._config.token_scope
            )
            self._client = AsyncOpenAI(
                base_url=self._config.base_url,
                api_key=_PLACEHOLDER_KEY,
                timeout=self._config.timeout_seconds,
            )
        except Exception as exc:
            self._failed = (
                f"could not construct model client: {type(exc).__name__}: {exc}"
            )
            raise ModelUnavailable(self._failed) from exc

        logger.info(
            "Model client ready deployment=%s base_url=%s",
            self._config.deployment,
            self._config.base_url,
        )

    async def complete(self, prompt: str, system_prompt: str) -> str:
        """Send one chat completion request and return the text response.

        The Microsoft OpenAI instrumentor wraps this call and emits the
        ``chat <model>`` span; nothing here creates a span.
        """
        self._ensure()
        token = self._token_provider()

        response = await self._client.chat.completions.create(
            model=self._config.deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            extra_headers={"Authorization": f"Bearer {token}"},
        )

        choices = getattr(response, "choices", None) or []
        if not choices:
            return ""
        content = getattr(choices[0].message, "content", None)
        return (content or "").strip()

    async def aclose(self) -> None:
        """Release the client and credential. Never raises."""
        for target in (self._client, self._credential):
            close = getattr(target, "close", None)
            if close is None:
                continue
            try:
                result = close()
                if hasattr(result, "__await__"):
                    await result
            except Exception:  # pragma: no cover - defensive
                logger.debug("model client close failed", exc_info=True)
        self._client = None
        self._credential = None


def build_model_client() -> "ModelClient | None":
    """Return a configured client, or ``None`` when no model is configured."""
    config = ModelConfig.from_environment()
    return ModelClient(config) if config else None


__all__ = [
    "ModelClient",
    "ModelConfig",
    "ModelUnavailable",
    "build_model_client",
    "PLATFORM_ENDPOINT_VAR",
    "ENDPOINT_OVERRIDE_VAR",
    "MODEL_DEPLOYMENT_VAR",
    "TOKEN_SCOPE_VAR",
]
