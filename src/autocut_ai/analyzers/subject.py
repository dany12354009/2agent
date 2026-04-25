from __future__ import annotations

from collections import Counter

from ..models import SubjectTrack
from .base import Analyzer, VideoMetadata


class SubjectAnalyzer(Analyzer):
    """Main-subject analysis with optional local models.

    Model usage:
    - YOLO (ultralytics): person/object detection per frame.
    - MediaPipe: face/body landmarks for better person focus.
    - OpenCV fallback: center-bias pseudo subject when models missing.
    """

    def run(self, metadata: VideoMetadata, frames: list) -> dict:
        tracks = self._run_yolo(frames)
        if not tracks:
            tracks = self._fallback_center_subject(metadata)

        main_id = self._select_main_subject(tracks)
        return {"detected_subjects": tracks, "main_subject_id": main_id}

    def _run_yolo(self, frames: list) -> list[SubjectTrack]:
        try:
            from ultralytics import YOLO  # type: ignore
        except Exception:
            return []

        model = YOLO("yolov8n.pt")
        tracks: dict[str, SubjectTrack] = {}
        for frame in frames:
            results = model(frame, verbose=False)
            for result in results:
                for box in result.boxes:
                    cls = int(box.cls.item())
                    label = model.names.get(cls, f"cls_{cls}")
                    conf = float(box.conf.item())
                    x1, y1, x2, y2 = [float(v) for v in box.xyxy[0].tolist()]
                    track_id = f"{label}_0"
                    if track_id not in tracks:
                        tracks[track_id] = SubjectTrack(id=track_id, label=label, confidence=conf)
                    tracks[track_id].boxes.append((x1, y1, x2, y2))
                    tracks[track_id].confidence = max(tracks[track_id].confidence, conf)
        return list(tracks.values())

    def _fallback_center_subject(self, metadata: VideoMetadata) -> list[SubjectTrack]:
        # Default synthetic subject enables full pipeline without heavy AI deps.
        x1, y1 = metadata.width * 0.25, metadata.height * 0.2
        x2, y2 = metadata.width * 0.75, metadata.height * 0.8
        return [
            SubjectTrack(
                id="primary_center_subject",
                label="salient_subject",
                confidence=0.4,
                boxes=[(x1, y1, x2, y2)],
            )
        ]

    def _select_main_subject(self, tracks: list[SubjectTrack]) -> str | None:
        if not tracks:
            return None
        weighted = Counter({t.id: t.confidence * max(len(t.boxes), 1) for t in tracks})
        return weighted.most_common(1)[0][0]
