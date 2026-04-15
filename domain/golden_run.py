from __future__ import annotations

from domain.models import BaselineComparison, FeatureSet, PhaseResult


class GoldenRunComparator:
    def compare(self, features: FeatureSet, phase: PhaseResult) -> BaselineComparison:
        golden_id = f"{phase.phase_name.lower().replace(' ', '_')}_baseline_v3"

        deviations = {
            "vibration_delta_pct": round(
                ((features.features.get("vibration_mean", 0.0) - 2.0) / 2.0) * 100.0, 2
            ),
            "temperature_delta_pct": round(
                ((features.features.get("temperature_mean", 0.0) - 55.0) / 55.0) * 100.0, 2
            ),
        }

        similarity = max(0.0, 1.0 - abs(deviations["vibration_delta_pct"]) / 100.0)

        return BaselineComparison(
            asset_id=features.asset_id,
            matched_golden_run_id=golden_id,
            similarity_score=round(similarity, 3),
            deviations=deviations,
            summary=(
                f"Matched {golden_id}; similarity={similarity:.3f}; "
                f"key deviations={deviations}"
            ),
        )
