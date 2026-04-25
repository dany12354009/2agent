from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AnalysisMode(str, Enum):
    LIGHT = "light"
    FULL = "full"


class OutputFormat(str, Enum):
    TIKTOK = "tiktok"
    SHORTS = "shorts"
    REELS = "reels"


@dataclass
class ModelConfig:
    detection_enabled: bool = True
    tracking_enabled: bool = True
    face_body_enabled: bool = True
    audio_enabled: bool = True
    whisper_enabled: bool = False
    mode: AnalysisMode = AnalysisMode.LIGHT


@dataclass
class ProductConfig:
    output_format: OutputFormat = OutputFormat.SHORTS
    target_aspect_ratio: tuple[int, int] = (9, 16)
    edit_intensity: float = 0.7
    use_gpu_if_available: bool = True
    watermark_enabled: bool = False
    batch_size: int = 4


@dataclass
class AppConfig:
    model: ModelConfig = field(default_factory=ModelConfig)
    product: ProductConfig = field(default_factory=ProductConfig)
