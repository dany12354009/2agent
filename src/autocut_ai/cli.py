from __future__ import annotations

import argparse
from pathlib import Path

from .engine import AutoCutEngine
from .exporters.capcut_exports import (
    export_effect_recommendations,
    export_keyframes_csv,
    export_timeline_json,
)
from .models import EditStyle


def main() -> None:
    parser = argparse.ArgumentParser(description="AutoCut AI local editing planner")
    parser.add_argument("video", help="Path to input video")
    parser.add_argument("--style", default=EditStyle.CLEAN_SHORTS.value, choices=[s.value for s in EditStyle])
    parser.add_argument("--out", default="autocut_output", help="Output folder")
    args = parser.parse_args()

    engine = AutoCutEngine()
    plan = engine.auto_edit(args.video, EditStyle(args.style))

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    t = export_timeline_json(plan, out_dir / "timeline.json")
    k = export_keyframes_csv(plan, out_dir / "keyframes.csv")
    e = export_effect_recommendations(plan, out_dir / "effects.json")

    print(f"Exported:\n- {t}\n- {k}\n- {e}")


if __name__ == "__main__":
    main()
