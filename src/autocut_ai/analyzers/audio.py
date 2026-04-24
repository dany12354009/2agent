from __future__ import annotations

from .base import Analyzer, VideoMetadata


class AudioBeatAnalyzer(Analyzer):
    """Local beat detection using librosa when installed."""

    def run(self, metadata: VideoMetadata, frames: list) -> dict:
        # `frames` is unused here; analyzer signature stays uniform.
        try:
            import librosa  # type: ignore
        except Exception:
            return {"beat_timestamps": []}

        try:
            y, sr = librosa.load(metadata.path, sr=None)
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            _ = tempo
            beat_timestamps = librosa.frames_to_time(beats, sr=sr).tolist()
            return {"beat_timestamps": beat_timestamps}
        except Exception:
            return {"beat_timestamps": []}
