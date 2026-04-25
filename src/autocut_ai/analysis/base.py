from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from ..video.engine import MultiResolutionFrames
from .graph import SceneIntelligenceGraph


@dataclass
class AnalysisContext:
    frames: MultiResolutionFrames
    gpu_available: bool
    settings: dict[str, Any]


class AnalysisModule(Protocol):
    name: str

    def run(self, context: AnalysisContext, graph: SceneIntelligenceGraph) -> None:
        ...
