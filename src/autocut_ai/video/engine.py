from __future__ import annotations

import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class VideoMetadata:
    path: str
    fps: float
    frame_count: int
    width: int
    height: int

    @property
    def duration_sec(self) -> float:
        return 0.0 if self.fps <= 0 else self.frame_count / self.fps


@dataclass
class MultiResolutionFrames:
    metadata: VideoMetadata
    frames_by_height: dict[int, list[Any]]


class VideoCache:
    def __init__(self, cache_dir: str = ".autocut_cache") -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _key(self, video_path: str, heights: list[int], sample_fps: float) -> str:
        raw = json.dumps({"path": video_path, "heights": heights, "sample_fps": sample_fps}, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(self, video_path: str, heights: list[int], sample_fps: float) -> MultiResolutionFrames | None:
        key = self._key(video_path, heights, sample_fps)
        meta_path = self.cache_dir / f"{key}.json"
        if not meta_path.exists():
            return None
        try:
            payload = json.loads(meta_path.read_text())
            metadata = VideoMetadata(**payload["metadata"])
            return MultiResolutionFrames(metadata=metadata, frames_by_height={})
        except Exception:
            return None

    def put(self, video_path: str, heights: list[int], sample_fps: float, metadata: VideoMetadata) -> None:
        key = self._key(video_path, heights, sample_fps)
        meta_path = self.cache_dir / f"{key}.json"
        meta_path.write_text(json.dumps({"metadata": metadata.__dict__}), encoding="utf-8")


class VideoProcessingEngine:
    def __init__(self, cache: VideoCache | None = None) -> None:
        self.cache = cache or VideoCache()

    def extract_frames(
        self,
        video_path: str,
        heights: list[int] | None = None,
        sample_fps: float = 6.0,
        use_cache: bool = True,
    ) -> MultiResolutionFrames:
        heights = heights or [360, 720]
        cached = self.cache.get(video_path, heights, sample_fps) if use_cache else None
        if cached is not None and cached.frames_by_height == {}:
            logger.info("Cache metadata hit for %s", video_path)

        try:
            import cv2  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("opencv-python is required") from exc

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
        metadata = VideoMetadata(video_path, fps, frame_count, width, height)

        sample_step = max(int(fps / max(sample_fps, 0.5)), 1)
        raw_frames: list[Any] = []
        idx = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if idx % sample_step == 0:
                raw_frames.append(frame)
            idx += 1
        cap.release()

        def _resize(target_h: int) -> tuple[int, list[Any]]:
            resized = []
            for frame in raw_frames:
                h, w = frame.shape[:2]
                scale = target_h / max(h, 1)
                target_w = max(int(w * scale), 1)
                resized.append(cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA))
            return target_h, resized

        frames_by_height: dict[int, list[Any]] = {}
        with ThreadPoolExecutor(max_workers=min(4, len(heights))) as pool:
            for target_h, frames in pool.map(_resize, heights):
                frames_by_height[target_h] = frames

        self.cache.put(video_path, heights, sample_fps, metadata)
        return MultiResolutionFrames(metadata=metadata, frames_by_height=frames_by_height)
