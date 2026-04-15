from app import build_demo_batch
from orchestrator.workflow import DigitalTwinWorkflow


def test_workflow_runs() -> None:
    workflow = DigitalTwinWorkflow(
        llm_config={"config_list": [{"model": "stub-gpt", "api_key": "x"}], "temperature": 0.2}
    )
    state = workflow.run(build_demo_batch())

    assert state.features is not None
    assert state.phase is not None
    assert state.baseline is not None
    assert state.risk is not None
    assert state.safety is not None
    assert state.action_plan is not None
