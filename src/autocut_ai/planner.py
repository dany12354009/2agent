from __future__ import annotations

from .analysis.graph import SceneIntelligenceGraph
from .decision.engine import DecisionEngine
from .models import EditPlan


class EditPlanner:
    """Compatibility planner built on top of the production DecisionEngine."""

    def build(self, source_video: str, style: str, graph: SceneIntelligenceGraph, intensity: float = 0.7) -> EditPlan:
        actions = DecisionEngine(style_name=style, intensity=intensity).build_actions(graph)
        return EditPlan(source_video=source_video, style=style, actions=actions)
