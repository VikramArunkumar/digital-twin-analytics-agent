from __future__ import annotations

from domain.models import FeatureSet, PhaseResult


class PhaseDetectionService:
    def detect_phase(self, features: FeatureSet) -> PhaseResult:
        load = features.features.get("load_mean", 0.0)

        if load < 20:
            phase = "Idle"
            conf = 0.93
        elif load < 70:
            phase = "Nominal Operation"
            conf = 0.89
        else:
            phase = "High Load Phase"
            conf = 0.91

        return PhaseResult(
            asset_id=features.asset_id,
            phase_name=phase,
            confidence=conf,
            evidence={
                "load_mean": load,
                "window": [features.window_start, features.window_end],
            },
        )
