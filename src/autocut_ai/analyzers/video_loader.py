from __future__ import annotations

from typing import Any

from .base import VideoMetadata


def load_video(video_path: str, sample_fps: float = 4.0) -> tuple[VideoMetadata, list[Any]]:
    """Load sparse frames using OpenCV when available.

    Keeping this isolated means users can swap in ffmpeg decoders later.
    """

    try:
        import cv2  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on optional deps
        raise RuntimeError("opencv-python is required for video loading") from exc

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    metadata = VideoMetadata(video_path, fps, frame_count, width, height)

    sample_step = max(int(fps / max(sample_fps, 0.1)), 1)
    frames = []
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % sample_step == 0:
            frames.append(frame)
        idx += 1

    cap.release()
    return metadata, frames
