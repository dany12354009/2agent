from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class EditStyle(str, Enum):
    GAMING_SHORT = "gaming_short"
    CINEMATIC = "cinematic"
    MEME = "meme"
    FAST_TIKTOK = "fast_tiktok"
    DRAMATIC_SLOWMO = "dramatic_slowmo"
    CLEAN_SHORTS = "clean_shorts"


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
class AnalysisResult:
    duration_sec: float
    scene_cuts: list[float]
    beat_timestamps: list[float]
    motion_spikes: list[float]
    detected_subjects: list[SubjectTrack]
    main_subject_id: str | None


@dataclass
class EditPlan:
    source_video: str
    style: EditStyle
    actions: list[TimelineAction]


STYLE_EFFECT_PRESETS: dict[EditStyle, dict[str, float]] = {
    EditStyle.GAMING_SHORT: {"zoom": 0.8, "shake": 0.9, "caption": 0.8},
    EditStyle.CINEMATIC: {"zoom": 0.4, "shake": 0.2, "slowmo": 0.6},
    EditStyle.MEME: {"zoom": 0.9, "flash": 0.8, "caption": 1.0},
    EditStyle.FAST_TIKTOK: {"zoom": 0.85, "beat_cut": 0.95, "caption": 0.9},
    EditStyle.DRAMATIC_SLOWMO: {"slowmo": 1.0, "zoom": 0.5, "flash": 0.4},
    EditStyle.CLEAN_SHORTS: {"zoom": 0.6, "beat_cut": 0.6, "caption": 0.5},
}
