from __future__ import annotations

from statistics import mean
from domain.models import FeatureSet, TelemetryBatch


class TelemetryMiningService:
    def extract_features(self, batch: TelemetryBatch) -> FeatureSet:
        if not batch.points:
            raise ValueError("Telemetry batch is empty")

        vibration = [p.values.get("vibration", 0.0) for p in batch.points]
        temperature = [p.values.get("temperature", 0.0) for p in batch.points]
        load = [p.values.get("load", 0.0) for p in batch.points]

        features = {
            "vibration_mean": round(mean(vibration), 3),
            "temperature_mean": round(mean(temperature), 3),
            "load_mean": round(mean(load), 3),
            "vibration_max": max(vibration),
            "temperature_max": max(temperature),
        }

        return FeatureSet(
            asset_id=batch.asset_id,
            window_start=batch.points[0].timestamp,
            window_end=batch.points[-1].timestamp,
            features=features,
            metadata={"num_points": len(batch.points)},
        )
