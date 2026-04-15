from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TelemetryPoint:
    timestamp: str
    tags: Dict[str, str]
    values: Dict[str, float]


@dataclass
class TelemetryBatch:
    asset_id: str
    points: List[TelemetryPoint]


@dataclass
class FeatureSet:
    asset_id: str
    window_start: str
    window_end: str
    features: Dict[str, float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PhaseResult:
    asset_id: str
    phase_name: str
    confidence: float
    evidence: Dict[str, Any]


@dataclass
class BaselineComparison:
    asset_id: str
    matched_golden_run_id: str
    similarity_score: float
    deviations: Dict[str, float]
    summary: str


@dataclass
class RiskAssessment:
    asset_id: str
    anomaly_score: float
    failure_probability_2h: float
    severity: str
    drivers: List[str]
    summary: str


@dataclass
class SafetyStatus:
    asset_id: str
    status: str
    breached_rules: List[str]
    summary: str


@dataclass
class RecommendedAction:
    title: str
    description: str
    priority: str
    expected_effect: str
    requires_human_approval: bool = True


@dataclass
class ActionPlan:
    asset_id: str
    reasoning: str
    actions: List[RecommendedAction]
    final_recommendation: str


@dataclass
class WorkflowState:
    telemetry: Optional[TelemetryBatch] = None
    features: Optional[FeatureSet] = None
    phase: Optional[PhaseResult] = None
    baseline: Optional[BaselineComparison] = None
    risk: Optional[RiskAssessment] = None
    safety: Optional[SafetyStatus] = None
    action_plan: Optional[ActionPlan] = None
