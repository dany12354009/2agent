from __future__ import annotations

from .base import Analyzer, VideoMetadata


class MotionIntensityAnalyzer(Analyzer):
    """Detects high-motion moments from frame difference magnitudes."""

    def __init__(self, spike_quantile: float = 0.85) -> None:
        self.spike_quantile = spike_quantile

    def run(self, metadata: VideoMetadata, frames: list) -> dict:
        if len(frames) < 2:
            return {"motion_spikes": []}

        try:
            import cv2  # type: ignore
            import numpy as np
        except Exception:
            return {"motion_spikes": []}

        mags: list[float] = []
        prev = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        for frame in frames[1:]:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(prev, gray)
            mags.append(float(diff.mean()))
            prev = gray

        if not mags:
            return {"motion_spikes": []}

        threshold = float(np.quantile(np.array(mags), self.spike_quantile))
        spikes = [
            (i + 1) * (metadata.duration_sec / max(len(frames), 1))
            for i, val in enumerate(mags)
            if val >= threshold
        ]
        return {"motion_spikes": spikes}
