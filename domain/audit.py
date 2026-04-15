from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from domain.models import WorkflowState


class AuditService:
    def __init__(self, output_dir: str = "audit_logs") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, state: WorkflowState) -> Path:
        asset_id = state.features.asset_id if state.features else "unknown_asset"
        path = self.output_dir / f"{asset_id}_latest.json"

        payload = {
            "features": asdict(state.features) if state.features else None,
            "phase": asdict(state.phase) if state.phase else None,
            "baseline": asdict(state.baseline) if state.baseline else None,
            "risk": asdict(state.risk) if state.risk else None,
            "safety": asdict(state.safety) if state.safety else None,
            "action_plan": asdict(state.action_plan) if state.action_plan else None,
        }

        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path
