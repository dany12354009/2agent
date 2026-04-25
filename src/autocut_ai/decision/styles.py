from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StyleProfile:
    name: str
    cut_speed: float
    zoom_intensity: float
    shake_enabled: bool
    caption_mode: str
    motion_blur: bool = False
    meme_effects: bool = False


STYLE_PROFILES: dict[str, StyleProfile] = {
    "gaming_short": StyleProfile("gaming_short", cut_speed=0.9, zoom_intensity=0.9, shake_enabled=True, caption_mode="bold"),
    "cinematic": StyleProfile("cinematic", cut_speed=0.35, zoom_intensity=0.35, shake_enabled=False, caption_mode="minimal", motion_blur=True),
    "viral_shorts": StyleProfile(
        "viral_shorts",
        cut_speed=1.0,
        zoom_intensity=1.0,
        shake_enabled=True,
        caption_mode="aggressive",
        meme_effects=True,
    ),
    "clean_shorts": StyleProfile("clean_shorts", cut_speed=0.6, zoom_intensity=0.5, shake_enabled=False, caption_mode="clean"),
}
