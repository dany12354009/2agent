from __future__ import annotations

from dataclasses import dataclass, field

from ..models import EditPlan, TimelineAction


@dataclass
class TimelineClip:
    track: str
    start_sec: float
    end_sec: float
    metadata: dict = field(default_factory=dict)


@dataclass
class TimelineProject:
    source_video: str
    actions: list[TimelineAction]
    video_track: list[TimelineClip]
    effects_track: list[TimelineClip]
    captions_track: list[TimelineClip]


class TimelineGenerator:
    def build(self, plan: EditPlan, duration_sec: float) -> TimelineProject:
        video_track = [TimelineClip("video", 0.0, duration_sec)]
        effects_track: list[TimelineClip] = []
        captions_track: list[TimelineClip] = []

        for action in plan.actions:
            if action.effect == "text_caption":
                captions_track.append(
                    TimelineClip(
                        "captions",
                        action.timestamp,
                        min(action.timestamp + 1.8, duration_sec),
                        {"reason": action.reason},
                    )
                )
            else:
                effects_track.append(
                    TimelineClip(
                        "effects",
                        action.timestamp,
                        min(action.timestamp + 0.4, duration_sec),
                        {"effect": action.effect, "intensity": action.intensity},
                    )
                )

        return TimelineProject(
            source_video=plan.source_video,
            actions=plan.actions,
            video_track=video_track,
            effects_track=effects_track,
            captions_track=captions_track,
        )
