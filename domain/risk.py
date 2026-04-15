from __future__ import annotations

from domain.models import BaselineComparison, FeatureSet, RiskAssessment


class RiskService:
    def assess(self, features: FeatureSet, baseline: BaselineComparison) -> RiskAssessment:
        vib = features.features.get("vibration_mean", 0.0)
        temp = features.features.get("temperature_mean", 0.0)

        anomaly = min(1.0, (vib / 5.0 + temp / 120.0) / 2.0)
        failure_prob = min(1.0, max(0.0, anomaly * 0.8))

        if failure_prob >= 0.7:
            severity = "CRITICAL"
        elif failure_prob >= 0.4:
            severity = "HIGH"
        elif failure_prob >= 0.2:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        drivers = []
        if vib > 3.5:
            drivers.append("Elevated vibration")
        if temp > 85:
            drivers.append("High temperature")
        if baseline.deviations.get("vibration_delta_pct", 0.0) > 15:
            drivers.append("Deviation from golden run")

        return RiskAssessment(
            asset_id=features.asset_id,
            anomaly_score=round(anomaly, 3),
            failure_probability_2h=round(failure_prob, 3),
            severity=severity,
            drivers=drivers,
            summary=f"Severity={severity}, failure_probability_2h={failure_prob:.3f}",
        )
