from autocut_ai.models import AnalysisResult, EditStyle, SubjectTrack
from autocut_ai.planner import EditPlanner


def test_planner_builds_sorted_actions() -> None:
    planner = EditPlanner()
    analysis = AnalysisResult(
        duration_sec=10.0,
        scene_cuts=[4.0],
        beat_timestamps=[1.0, 3.0],
        motion_spikes=[2.0],
        detected_subjects=[SubjectTrack(id="s1", label="person", confidence=0.9)],
        main_subject_id="s1",
    )

    plan = planner.build("clip.mp4", EditStyle.FAST_TIKTOK, analysis)
    assert [a.timestamp for a in plan.actions] == [1.0, 2.0, 3.0, 4.0]
    assert any(a.effect == "beat_cut" for a in plan.actions)
