from __future__ import annotations

from domain.models import TelemetryBatch, TelemetryPoint, WorkflowState
from orchestrator.workflow import DigitalTwinWorkflow
from domain.audit import AuditService


def build_demo_batch() -> TelemetryBatch:
    points = [
        TelemetryPoint(
            timestamp="2026-04-13T10:00:00Z",
            tags={"machine": "press_07"},
            values={"vibration": 3.8, "temperature": 78.0, "load": 82.0},
        ),
        TelemetryPoint(
            timestamp="2026-04-13T10:01:00Z",
            tags={"machine": "press_07"},
            values={"vibration": 4.1, "temperature": 81.0, "load": 84.0},
        ),
        TelemetryPoint(
            timestamp="2026-04-13T10:02:00Z",
            tags={"machine": "press_07"},
            values={"vibration": 4.4, "temperature": 83.0, "load": 86.0},
        ),
    ]
    return TelemetryBatch(asset_id="press_07", points=points)


def require_human_review(state: WorkflowState) -> bool:
    if state.action_plan is None:
        return True
    if any(action.requires_human_approval for action in state.action_plan.actions):
        return True
    if state.safety and state.safety.status in {"WARNING", "CRITICAL"}:
        return True
    return False


def main() -> None:
    llm_config = {
        "config_list": [{"model": "stub-gpt", "api_key": "optional-for-stubs"}],
        "temperature": 0.2,
    }

    workflow = DigitalTwinWorkflow(llm_config=llm_config)
    audit = AuditService()

    telemetry_batch = build_demo_batch()
    state = workflow.run(telemetry_batch)

    print("\n=== Phase ===")
    print(state.phase)

    print("\n=== Baseline ===")
    print(state.baseline)

    print("\n=== Risk ===")
    print(state.risk)

    print("\n=== Safety ===")
    print(state.safety)

    print("\n=== Action Plan ===")
    print(state.action_plan)

    print("\n=== Human Review ===")
    print("Required" if require_human_review(state) else "Not required")

    path = audit.save(state)
    print(f"\nSaved audit log to: {path}")


if __name__ == "__main__":
    main()
