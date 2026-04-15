from __future__ import annotations

from domain.models import TelemetryBatch, WorkflowState
from crews.telemetry_crew import TelemetryPipelineCrew
from autogen_layer.group_chat import ActionReasoningEngine


class DigitalTwinWorkflow:
    def __init__(self, llm_config: dict) -> None:
        self.pipeline_crew = TelemetryPipelineCrew()
        self.reasoning_engine = ActionReasoningEngine(llm_config=llm_config)

    def run(self, telemetry_batch: TelemetryBatch) -> WorkflowState:
        state = WorkflowState(telemetry=telemetry_batch)
        state = self.pipeline_crew.run(state)
        state.action_plan = self.reasoning_engine.generate_action_plan(state)
        return state
