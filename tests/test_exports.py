import json

from autocut_ai.exporters.capcut_exports import export_timeline_json
from autocut_ai.models import EditPlan, TimelineAction


def test_export_timeline_json(tmp_path) -> None:
    plan = EditPlan(
        source_video="in.mp4",
        style="clean_shorts",
        actions=[
            TimelineAction(
                timestamp=1.2,
                action="cut_to_beat",
                effect="beat_cut",
                tracking_target="subject",
                intensity=0.6,
                reason="Audio beat peak",
            )
        ],
    )

    out = tmp_path / "timeline.json"
    export_timeline_json(plan, out)
    payload = json.loads(out.read_text())
    assert payload["source_video"] == "in.mp4"
    assert payload["style"] == "clean_shorts"
