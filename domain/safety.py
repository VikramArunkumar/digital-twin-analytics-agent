from __future__ import annotations

from domain.models import FeatureSet, RiskAssessment, SafetyStatus


class SafetyService:
    def evaluate(self, features: FeatureSet, risk: RiskAssessment) -> SafetyStatus:
        breached = []

        if features.features.get("temperature_max", 0.0) > 95:
            breached.append("TEMP_LIMIT_EXCEEDED")
        if features.features.get("vibration_max", 0.0) > 5.5:
            breached.append("VIBRATION_LIMIT_EXCEEDED")
        if risk.failure_probability_2h > 0.75:
            breached.append("FAILURE_PROBABILITY_CRITICAL")

        if "TEMP_LIMIT_EXCEEDED" in breached or "VIBRATION_LIMIT_EXCEEDED" in breached:
            status = "CRITICAL"
        elif breached:
            status = "WARNING"
        else:
            status = "OK"

        return SafetyStatus(
            asset_id=features.asset_id,
            status=status,
            breached_rules=breached,
            summary=f"Safety status={status}, breached_rules={breached}",
        )
