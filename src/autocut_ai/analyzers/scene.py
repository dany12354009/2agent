from __future__ import annotations

from .base import Analyzer, VideoMetadata


class SceneChangeAnalyzer(Analyzer):
    """Simple histogram-diff scene detection via OpenCV.

    This is lightweight and local-only. Can be replaced with deep models later.
    """

    def __init__(self, threshold: float = 0.45) -> None:
        self.threshold = threshold

    def run(self, metadata: VideoMetadata, frames: list) -> dict:
        if not frames:
            return {"scene_cuts": []}

        try:
            import cv2  # type: ignore
        except Exception:
            return {"scene_cuts": []}

        scene_cuts: list[float] = []
        prev_hist = None
        for i, frame in enumerate(frames):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            hist = cv2.calcHist([gray], [0], None, [32], [0, 256])
            hist = cv2.normalize(hist, hist).flatten()
            if prev_hist is not None:
                score = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_BHATTACHARYYA)
                if score > self.threshold:
                    ts = i * (metadata.duration_sec / max(len(frames), 1))
                    scene_cuts.append(ts)
            prev_hist = hist
        return {"scene_cuts": scene_cuts}
