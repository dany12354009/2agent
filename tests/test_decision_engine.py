from autocut_ai.analysis.graph import SceneIntelligenceGraph, TimeEvent
from autocut_ai.decision.engine import DecisionEngine


def test_decision_engine_applies_rhythm_and_motion_rules() -> None:
    graph = SceneIntelligenceGraph(duration_sec=12.0)
    graph.upsert_subject("p1", "person", 0.9)
    graph.add_event(TimeEvent(1.0, "beat", 0.8, {}))
    graph.add_event(TimeEvent(1.2, "action_spike", 0.9, {}))
    graph.add_event(TimeEvent(1.3, "action_spike", 0.95, {}))

    actions = DecisionEngine(style_name="gaming_short", intensity=0.9).build_actions(graph)
    effects = [a.effect for a in actions]

    assert "beat_cut" in effects
    assert "zoom_in" in effects
    # shake spam should be smoothed.
    assert effects.count("shake") == 1
