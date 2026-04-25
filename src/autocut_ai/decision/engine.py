from __future__ import annotations

from dataclasses import dataclass

from ..analysis.graph import SceneIntelligenceGraph
from ..models import TimelineAction
from .styles import STYLE_PROFILES, StyleProfile


@dataclass
class DecisionEngine:
    style_name: str
    intensity: float = 0.7

    def build_actions(self, graph: SceneIntelligenceGraph) -> list[TimelineAction]:
        style = STYLE_PROFILES.get(self.style_name, STYLE_PROFILES["clean_shorts"])
        main_subject = self._pick_subject(graph)

        actions: list[TimelineAction] = []
        for event in sorted(graph.events, key=lambda e: e.time_sec):
            attention = self._attention_score(event.confidence, style)
            if event.event_type == "action_spike":
                actions.append(
                    TimelineAction(
                        timestamp=event.time_sec,
                        action="focus_subject",
                        effect="zoom_in",
                        tracking_target=main_subject,
                        intensity=min(style.zoom_intensity * attention, 1.0),
                        reason="Attention model: action + motion",
                    )
                )
                if style.shake_enabled and attention > 0.6:
                    actions.append(
                        TimelineAction(
                            timestamp=event.time_sec,
                            action="impact_emphasis",
                            effect="shake",
                            tracking_target=main_subject,
                            intensity=min(attention * self.intensity, 1.0),
                            reason="Cinematic rule: limited shake on high-impact frames",
                        )
                    )
            elif event.event_type == "beat":
                actions.append(
                    TimelineAction(
                        timestamp=event.time_sec,
                        action="rhythm_cut",
                        effect="beat_cut",
                        tracking_target=main_subject,
                        intensity=min(style.cut_speed * self.intensity, 1.0),
                        reason="Rhythm engine: beat-aligned cut",
                    )
                )
            elif event.event_type == "scene_cut":
                actions.append(
                    TimelineAction(
                        timestamp=event.time_sec,
                        action="transition",
                        effect="flash" if style.meme_effects else "crossfade",
                        tracking_target=main_subject,
                        intensity=0.5,
                        reason="Visual continuity rule on detected scene boundary",
                    )
                )
            elif event.event_type == "speech":
                text = event.payload.get("text", "")
                actions.append(
                    TimelineAction(
                        timestamp=event.time_sec,
                        action="caption",
                        effect="text_caption",
                        tracking_target=main_subject,
                        intensity=0.8 if style.caption_mode in {"bold", "aggressive"} else 0.5,
                        reason=f"Speech transcription for caption: {text[:48]}",
                    )
                )

        return self._smooth_actions(actions)

    def _pick_subject(self, graph: SceneIntelligenceGraph) -> str:
        if not graph.subjects:
            return "center_fallback"
        subject = max(graph.subjects.values(), key=lambda s: (s.confidence, len(s.boxes)))
        if subject.confidence < 0.4:
            graph.low_confidence_warnings.append("Main subject confidence low; manual override advised.")
        return subject.subject_id

    def _attention_score(self, confidence: float, style: StyleProfile) -> float:
        center_bias = 0.8
        return max(0.2, min(1.0, (confidence * 0.6 + center_bias * 0.4) * self.intensity * (0.7 + style.zoom_intensity * 0.3)))

    def _smooth_actions(self, actions: list[TimelineAction]) -> list[TimelineAction]:
        if not actions:
            return actions
        smooth: list[TimelineAction] = [actions[0]]
        last_shake_ts = actions[0].timestamp if actions[0].effect == "shake" else -999.0
        for action in actions[1:]:
            if action.effect == "shake" and action.timestamp - last_shake_ts < 0.35:
                # Cinematic anti-spam rule for shake.
                continue
            smooth.append(action)
            if action.effect == "shake":
                last_shake_ts = action.timestamp
        return smooth
