from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from ..models import EditPlan


def export_timeline_json(plan: EditPlan, output_path: str) -> Path:
    path = Path(output_path)
    path.write_text(json.dumps(asdict(plan), indent=2), encoding="utf-8")
    return path


def export_keyframes_csv(plan: EditPlan, output_path: str) -> Path:
    path = Path(output_path)
    lines = ["timestamp,effect,target,intensity"]
    for action in plan.actions:
        lines.append(
            f"{action.timestamp:.3f},{action.effect},{action.tracking_target},{action.intensity:.2f}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def export_effect_recommendations(plan: EditPlan, output_path: str) -> Path:
    grouped: dict[str, list[dict]] = {}
    for action in plan.actions:
        grouped.setdefault(action.effect, []).append(
            {
                "timestamp": action.timestamp,
                "reason": action.reason,
                "intensity": action.intensity,
            }
        )
    path = Path(output_path)
    path.write_text(json.dumps(grouped, indent=2), encoding="utf-8")
    return path
