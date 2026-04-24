from __future__ import annotations

from dataclasses import dataclass


@dataclass
class VideoMetadata:
    path: str
    fps: float
    frame_count: int
    width: int
    height: int

    @property
    def duration_sec(self) -> float:
        if self.fps <= 0:
            return 0.0
        return self.frame_count / self.fps


class Analyzer:
    """Base class for all analyzers to keep pipeline extensible."""

    def run(self, metadata: VideoMetadata, frames: list) -> dict:
        raise NotImplementedError
