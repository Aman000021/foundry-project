"""Minimal Microsoft Foundry Hosted Agent with model and workflow telemetry.

The golden image owns OpenTelemetry initialization. This module emits only the
Nestle workflow/step layer; Microsoft instrumentation emits the model span.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any, Final

from azure.ai.agentserver.responses import (
    InMemoryResponseProvider,
    ResponsesAgentServerHost,
    TextResponse,
)

from .model_client import ModelUnavailable, build_model_client

logger = logging.getLogger(__name__)

WORKFLOW_NAME: Final = os.environ["NESTLE_AGENT_WORKFLOW_NAME"]
STEP_ANSWER: Final = "answer"

SYSTEM_PROMPT: Final = (
    "You are a Nestle Foundry hosted agent used to validate platform "
    "telemetry. Answer clearly and concisely."
)

OUTCOME_ANSWERED: Final = "answered"
OUTCOME_ECHOED: Final = "echoed-no-model"
OUTCOME_EMPTY_INPUT: Final = "empty-input"
OUTCOME_MODEL_ERROR: Final = "model-error"


@dataclass(frozen=True)
class Answer:
    """Result of handling one request."""

    text: str
    outcome: str
    error_type: str | None = None
    error_detail: str = ""

    @property
    def failed(self) -> bool:
        return self.error_type is not None


app = ResponsesAgentServerHost(store=InMemoryResponseProvider())

# Configuration is resolved at import time; the client opens connections lazily.
_model = build_model_client()


def _get_workflow() -> Any:
    """Return golden-image workflow instrumentation when available."""
    try:
        from agenthost.observability import get_workflow

        return get_workflow(WORKFLOW_NAME)
    except Exception:
        logger.debug(
            "Golden-image observability unavailable; workflow spans disabled",
            exc_info=True,
        )
        return None


_workflow = _get_workflow()


async def _answer(user_text: str) -> Answer:
    """Return the response and telemetry outcome."""
    if not user_text:
        return Answer("No textual input was provided.", OUTCOME_EMPTY_INPUT)

    if _model is None:
        return Answer(
            f"Hosted Agent is running without a model. Received: {user_text}",
            OUTCOME_ECHOED,
        )

    try:
        reply = await _model.complete(user_text, SYSTEM_PROMPT)
    except ModelUnavailable as exc:
        logger.error("Model unavailable: %s", exc)
        return Answer(
            f"The model is not available: {exc}",
            OUTCOME_MODEL_ERROR,
            error_type=type(exc).__name__,
            error_detail=str(exc),
        )
    except Exception as exc:
        logger.exception("Model call failed")
        return Answer(
            f"The model call failed: {type(exc).__name__}: {exc}",
            OUTCOME_MODEL_ERROR,
            error_type=type(exc).__name__,
            error_detail=str(exc),
        )

    if not reply:
        return Answer(
            "The model returned an empty response.",
            OUTCOME_MODEL_ERROR,
            error_type="EmptyModelResponse",
            error_detail="The model returned no content",
        )

    return Answer(reply, OUTCOME_ANSWERED)


@app.response_handler
async def handle_response(
    request: Any,
    context: Any,
    cancellation_signal: Any,
) -> TextResponse:
    """Handle one Responses API request."""
    del cancellation_signal

    # CreateResponse input is represented as response input items. The SDK
    # context resolves references and combines the input_text content.
    user_text = (await context.get_input_text()).strip()

    logger.info(
        "Hosted Agent request received: input_present=%s model_configured=%s",
        bool(user_text),
        _model is not None,
    )

    if _workflow is None:
        answer = await _answer(user_text)
        return TextResponse(context=context, request=request, text=answer.text)

    # The model call occurs while step.answer is current. Microsoft model spans
    # therefore inherit the step as their parent through the ambient OTel context.
    with _workflow.workflow() as run:
        with run.step(STEP_ANSWER) as step:
            answer = await _answer(user_text)

            # Requires the golden-image workflow.py set_error update. Preserve
            # the response while exposing handled model failures in telemetry.
            if answer.failed and step is not None:
                set_error = getattr(step, "set_error", None)
                if callable(set_error):
                    set_error(
                        answer.error_type or "Error",
                        answer.error_detail,
                    )

        run.set_business_outcome(answer.outcome)

    return TextResponse(context=context, request=request, text=answer.text)


def main() -> None:
    """Start the Foundry Responses host."""
    logger.info(
        "Starting hosted agent workflow=%s model=%s",
        WORKFLOW_NAME,
        _model.deployment if _model else "none (echo mode)",
    )
    app.run()
