from __future__ import annotations

import json

from domain.models import ActionPlan, RecommendedAction, WorkflowState
from framework_stubs import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen_layer.prompts import SYSTEM_PROMPTS


class ActionReasoningEngine:
    def __init__(self, llm_config: dict) -> None:
        self.phase_expert = AssistantAgent(
            name="phase_expert",
            system_message=SYSTEM_PROMPTS["phase_expert"],
            llm_config=llm_config,
        )
        self.risk_expert = AssistantAgent(
            name="risk_expert",
            system_message=SYSTEM_PROMPTS["risk_expert"],
            llm_config=llm_config,
        )
        self.safety_expert = AssistantAgent(
            name="safety_expert",
            system_message=SYSTEM_PROMPTS["safety_expert"],
            llm_config=llm_config,
        )
        self.advisor = AssistantAgent(
            name="advisor",
            system_message=SYSTEM_PROMPTS["advisor"],
            llm_config=llm_config,
        )
        self.controller = UserProxyAgent(
            name="controller",
            human_input_mode="NEVER",
            code_execution_config=False,
        )

    def build_prompt(self, state: WorkflowState) -> str:
        if not all([state.features, state.phase, state.baseline, state.risk, state.safety]):
            raise ValueError("Workflow state incomplete for reasoning")

        payload = {
            "asset_id": state.features.asset_id,
            "features": state.features.features,
            "phase": {
                "phase_name": state.phase.phase_name,
                "confidence": state.phase.confidence,
                "evidence": state.phase.evidence,
            },
            "baseline": {
                "matched_golden_run_id": state.baseline.matched_golden_run_id,
                "similarity_score": state.baseline.similarity_score,
                "deviations": state.baseline.deviations,
                "summary": state.baseline.summary,
            },
            "risk": {
                "anomaly_score": state.risk.anomaly_score,
                "failure_probability_2h": state.risk.failure_probability_2h,
                "severity": state.risk.severity,
                "drivers": state.risk.drivers,
                "summary": state.risk.summary,
            },
            "safety": {
                "status": state.safety.status,
                "breached_rules": state.safety.breached_rules,
                "summary": state.safety.summary,
            },
        }

        return (
            "Review the digital twin telemetry state and produce a corrective action plan.\n"
            "Use only the supplied data.\n\n"
            f"{json.dumps(payload, indent=2)}"
        )

    def generate_action_plan(self, state: WorkflowState) -> ActionPlan:
        prompt = self.build_prompt(state)

        chat = GroupChat(
            agents=[
                self.controller,
                self.phase_expert,
                self.risk_expert,
                self.safety_expert,
                self.advisor,
            ],
            messages=[],
            max_round=8,
        )

        manager = GroupChatManager(groupchat=chat, llm_config=getattr(self.advisor, "llm_config", {}))
        result = self.controller.initiate_chat(manager, message=prompt)
        reasoning_text = getattr(result, "summary", None) or str(result)

        actions = self._heuristic_actions(state)

        return ActionPlan(
            asset_id=state.features.asset_id,
            reasoning=reasoning_text,
            actions=actions,
            final_recommendation=actions[0].description if actions else "Continue monitoring",
        )

    def _heuristic_actions(self, state: WorkflowState) -> list[RecommendedAction]:
        actions: list[RecommendedAction] = []

        if state.risk and state.risk.failure_probability_2h >= 0.4:
            actions.append(
                RecommendedAction(
                    title="Reduce machine load",
                    description="Reduce load by 10-15% for the next operating window.",
                    priority="HIGH",
                    expected_effect="Should reduce stress and vibration excursion risk.",
                    requires_human_approval=True,
                )
            )

        if state.safety and state.safety.status in {"WARNING", "CRITICAL"}:
            actions.append(
                RecommendedAction(
                    title="Inspect rotating assembly",
                    description="Inspect bearing/alignment condition at next safe pause.",
                    priority="HIGH",
                    expected_effect="May confirm mechanical source of elevated vibration.",
                    requires_human_approval=True,
                )
            )

        if not actions:
            actions.append(
                RecommendedAction(
                    title="Continue monitoring",
                    description="No immediate intervention; maintain enhanced monitoring.",
                    priority="MEDIUM",
                    expected_effect="Preserves production while collecting more evidence.",
                    requires_human_approval=False,
                )
            )

        return actions
