import logging, uuid
from dotenv import load_dotenv
from deploy_telemetry import DEPLOY_LOGGER, init_deploy_telemetry

from pathlib import Path
load_dotenv(Path(__file__).resolve().parent / ".env.deploy", override=True)

logging.basicConfig(level=logging.INFO)
t = init_deploy_telemetry()
log = logging.getLogger(DEPLOY_LOGGER)
print("destinations:", t.destinations)

run_id = str(uuid.uuid4())
with t.tracer.start_as_current_span("workflow.deploy-smoke-test",
        attributes={"run.id": run_id, "trigger.type": "test"}) as span:
    log.info("deploy telemetry smoke test run.id=%s", run_id)
    print(f"trace_id={span.get_span_context().trace_id:032x} run.id={run_id}")
t.shutdown()