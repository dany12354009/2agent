from autocut_ai.models import EditPlan, TimelineAction
from autocut_ai.services.product_service import ProcessingResult
from autocut_ai.timeline.generator import TimelineGenerator
from autocut_ai.tui.views import TUIViewModel, render_header, render_result_lines


def test_tui_header_contains_controls_state() -> None:
    model = TUIViewModel(video_path="clip.mp4", style="gaming_short", intensity=0.8)
    lines = render_header(model)
    assert any("clip.mp4" in line for line in lines)
    assert any("gaming_short" in line for line in lines)


def test_tui_result_render_includes_warnings() -> None:
    plan = EditPlan(
        source_video="clip.mp4",
        style="clean_shorts",
        actions=[TimelineAction(1.0, "focus", "zoom_in", "p1", 0.8, "motion")],
    )
    timeline = TimelineGenerator().build(plan, duration_sec=5.0)
    result = ProcessingResult(plan=plan, timeline=timeline, warnings=["low confidence"])

    lines = render_result_lines(result)
    assert any("zoom_in" in line for line in lines)
    assert any("low confidence" in line for line in lines)
