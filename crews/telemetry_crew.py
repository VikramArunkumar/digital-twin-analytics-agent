from __future__ import annotations

from dataclasses import asdict

from framework_stubs import CrewAgent, Crew, CrewTask, Process
from domain.models import WorkflowState
from crews.tasks import PipelineTasks


class TelemetryPipelineCrew:
    def __init__(self) -> None:
        self.pipeline = PipelineTasks()

        self.telemetry_agent = CrewAgent(
            role="Telemetry Analyst",
            goal="Convert raw telemetry into machine-health features",
            backstory="Specialist in signal conditioning and feature extraction.",
            verbose=True,
        )
        self.phase_agent = CrewAgent(
            role="Phase Detection Specialist",
            goal="Identify current asset operating phase",
            backstory="Expert in process-state classification.",
            verbose=True,
        )
        self.baseline_agent = CrewAgent(
            role="Golden Run Comparator",
            goal="Compare current behavior with known-good baseline",
            backstory="Expert in baseline matching and drift detection.",
            verbose=True,
        )
        self.risk_agent = CrewAgent(
            role="Risk Analyst",
            goal="Estimate anomaly severity and near-term failure risk",
            backstory="Reliability engineer focused on operational forecasting.",
            verbose=True,
        )
        self.safety_agent = CrewAgent(
            role="Safety Supervisor",
            goal="Check rule violations and safety constraints",
            backstory="Guardian of safe operating boundaries.",
            verbose=True,
        )

        self.crew = Crew(
            agents=[
                self.telemetry_agent,
                self.phase_agent,
                self.baseline_agent,
                self.risk_agent,
                self.safety_agent,
            ],
            tasks=[
                CrewTask(description="Extract telemetry features", agent=self.telemetry_agent),
                CrewTask(description="Detect operating phase", agent=self.phase_agent),
                CrewTask(description="Compare to golden run", agent=self.baseline_agent),
                CrewTask(description="Assess risk", agent=self.risk_agent),
                CrewTask(description="Evaluate safety", agent=self.safety_agent),
            ],
            process=Process.sequential,
            verbose=True,
        )

    def run(self, state: WorkflowState) -> WorkflowState:
        self.pipeline.run_telemetry_mining(state)
        self.pipeline.run_phase_detection(state)
        self.pipeline.run_golden_run_comparison(state)
        self.pipeline.run_risk_assessment(state)
        self.pipeline.run_safety_evaluation(state)
        return state

    def summarize_for_reasoning(self, state: WorkflowState) -> dict:
        return {
            "features": asdict(state.features) if state.features else None,
            "phase": asdict(state.phase) if state.phase else None,
            "baseline": asdict(state.baseline) if state.baseline else None,
            "risk": asdict(state.risk) if state.risk else None,
            "safety": asdict(state.safety) if state.safety else None,
        }
