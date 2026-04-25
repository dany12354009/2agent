from autocut_ai.models import EditPlan, TimelineAction
from autocut_ai.timeline.generator import TimelineGenerator


def test_timeline_generator_creates_layer_tracks() -> None:
    plan = EditPlan(
        source_video="input.mp4",
        style="clean_shorts",
        actions=[
            TimelineAction(0.5, "caption", "text_caption", "s1", 0.6, "hello"),
            TimelineAction(1.0, "focus", "zoom_in", "s1", 0.8, "motion"),
        ],
    )

    project = TimelineGenerator().build(plan, duration_sec=5.0)

    assert len(project.video_track) == 1
    assert len(project.captions_track) == 1
    assert len(project.effects_track) == 1
