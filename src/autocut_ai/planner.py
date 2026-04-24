from __future__ import annotations

from .models import AnalysisResult, EditPlan, EditStyle, STYLE_EFFECT_PRESETS, TimelineAction


class EditPlanner:
    """Converts analysis outputs into a CapCut-friendly edit plan."""

    def build(self, source_video: str, style: EditStyle, analysis: AnalysisResult) -> EditPlan:
        preset = STYLE_EFFECT_PRESETS[style]
        actions: list[TimelineAction] = []
        target = analysis.main_subject_id or "none"

        for ts in analysis.motion_spikes:
            actions.append(
                TimelineAction(
                    timestamp=ts,
                    action="emphasize_action",
                    effect="zoom_in",
                    tracking_target=target,
                    intensity=preset.get("zoom", 0.5),
                    reason="High motion intensity detected",
                )
            )

        for ts in analysis.beat_timestamps:
            actions.append(
                TimelineAction(
                    timestamp=ts,
                    action="cut_to_beat",
                    effect="beat_cut",
                    tracking_target=target,
                    intensity=preset.get("beat_cut", 0.7),
                    reason="Audio beat peak",
                )
            )

        for ts in analysis.scene_cuts:
            actions.append(
                TimelineAction(
                    timestamp=ts,
                    action="scene_transition",
                    effect="flash",
                    tracking_target=target,
                    intensity=preset.get("flash", 0.5),
                    reason="Scene boundary",
                )
            )

        actions.sort(key=lambda a: a.timestamp)
        return EditPlan(source_video=source_video, style=style, actions=actions)
