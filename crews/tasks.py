from __future__ import annotations

from domain.models import WorkflowState
from domain.telemetry import TelemetryMiningService
from domain.phase_detection import PhaseDetectionService
from domain.golden_run import GoldenRunComparator
from domain.risk import RiskService
from domain.safety import SafetyService


class PipelineTasks:
    def __init__(self) -> None:
        self.telemetry_service = TelemetryMiningService()
        self.phase_service = PhaseDetectionService()
        self.golden_service = GoldenRunComparator()
        self.risk_service = RiskService()
        self.safety_service = SafetyService()

    def run_telemetry_mining(self, state: WorkflowState) -> WorkflowState:
        if state.telemetry is None:
            raise ValueError("Missing telemetry in workflow state")
        state.features = self.telemetry_service.extract_features(state.telemetry)
        return state

    def run_phase_detection(self, state: WorkflowState) -> WorkflowState:
        if state.features is None:
            raise ValueError("Missing features in workflow state")
        state.phase = self.phase_service.detect_phase(state.features)
        return state

    def run_golden_run_comparison(self, state: WorkflowState) -> WorkflowState:
        if state.features is None or state.phase is None:
            raise ValueError("Missing features or phase in workflow state")
        state.baseline = self.golden_service.compare(state.features, state.phase)
        return state

    def run_risk_assessment(self, state: WorkflowState) -> WorkflowState:
        if state.features is None or state.baseline is None:
            raise ValueError("Missing features or baseline in workflow state")
        state.risk = self.risk_service.assess(state.features, state.baseline)
        return state

    def run_safety_evaluation(self, state: WorkflowState) -> WorkflowState:
        if state.features is None or state.risk is None:
            raise ValueError("Missing features or risk in workflow state")
        state.safety = self.safety_service.evaluate(state.features, state.risk)
        return state
