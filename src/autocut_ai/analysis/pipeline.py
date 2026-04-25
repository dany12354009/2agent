from __future__ import annotations

from dataclasses import dataclass

from ..core.config import AppConfig
from ..core.logging import get_logger
from ..video.engine import MultiResolutionFrames
from .base import AnalysisContext
from .graph import SceneIntelligenceGraph
from .modules import (
    AudioModule,
    DetectionModule,
    FaceBodyModule,
    MotionModule,
    SceneTransitionModule,
    TrackingModule,
    WhisperModule,
)

logger = get_logger(__name__)


@dataclass
class AnalysisPipeline:
    config: AppConfig

    def run(self, frames: MultiResolutionFrames) -> SceneIntelligenceGraph:
        graph = SceneIntelligenceGraph(duration_sec=frames.metadata.duration_sec)
        context = AnalysisContext(
            frames=frames,
            gpu_available=self._gpu_available() if self.config.product.use_gpu_if_available else False,
            settings={"mode": self.config.model.mode.value},
        )

        modules = [
            DetectionModule(),
            TrackingModule(),
            FaceBodyModule(),
            SceneTransitionModule(),
            MotionModule(),
        ]
        if self.config.model.audio_enabled:
            modules.append(AudioModule())
        if self.config.model.whisper_enabled:
            modules.append(WhisperModule())

        for module in modules:
            if not self._module_enabled(module.name):
                continue
            logger.info("Running analysis module: %s", module.name)
            module.run(context, graph)

        if not graph.subjects:
            graph.low_confidence_warnings.append("No subjects detected; center framing fallback recommended.")
        return graph

    def _module_enabled(self, name: str) -> bool:
        m = self.config.model
        mapping = {
            "detection": m.detection_enabled,
            "tracking": m.tracking_enabled,
            "face_body": m.face_body_enabled,
            "audio": m.audio_enabled,
            "whisper": m.whisper_enabled,
            "scene_transition": True,
            "motion": True,
        }
        return mapping.get(name, True)

    def _gpu_available(self) -> bool:
        try:
            import torch  # type: ignore

            return bool(torch.cuda.is_available())
        except Exception:
            return False
