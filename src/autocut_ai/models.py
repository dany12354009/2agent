from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SubjectTrack:
    id: str
    label: str
    confidence: float
    boxes: list[tuple[float, float, float, float]] = field(default_factory=list)


@dataclass
class TimelineAction:
    timestamp: float
    action: str
    effect: str
    tracking_target: str
    intensity: float
    reason: str


@dataclass
class EditPlan:
    source_video: str
    style: str
    actions: list[TimelineAction]
