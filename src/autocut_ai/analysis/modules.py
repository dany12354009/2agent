from __future__ import annotations

from statistics import mean

from .base import AnalysisContext
from .graph import SceneIntelligenceGraph, TimeEvent


class DetectionModule:
    name = "detection"

    def run(self, context: AnalysisContext, graph: SceneIntelligenceGraph) -> None:
        frames = context.frames.frames_by_height[min(context.frames.frames_by_height.keys())]
        try:
            from ultralytics import YOLO  # type: ignore
        except Exception:
            # Lightweight fallback if YOLO is unavailable.
            w = context.frames.metadata.width
            h = context.frames.metadata.height
            graph.upsert_subject("fallback_subject", "salient_subject", 0.35, (w * 0.25, h * 0.2, w * 0.75, h * 0.8))
            graph.low_confidence_warnings.append("YOLO unavailable; fallback center subject used.")
            return

        model = YOLO("yolov8n.pt")
        for frame in frames:
            results = model(frame, verbose=False)
            for result in results:
                for box in result.boxes:
                    cls = int(box.cls.item())
                    label = model.names.get(cls, f"cls_{cls}")
                    conf = float(box.conf.item())
                    x1, y1, x2, y2 = [float(v) for v in box.xyxy[0].tolist()]
                    graph.upsert_subject(f"{label}_0", label, conf, (x1, y1, x2, y2))


class TrackingModule:
    name = "tracking"

    def run(self, context: AnalysisContext, graph: SceneIntelligenceGraph) -> None:
        # Production hook: replace with SORT/DeepSORT. Fallback uses existing detection tracks.
        for subject in graph.subjects.values():
            if not subject.boxes:
                graph.low_confidence_warnings.append(f"Tracking weak for {subject.subject_id}; no boxes.")


class FaceBodyModule:
    name = "face_body"

    def run(self, context: AnalysisContext, graph: SceneIntelligenceGraph) -> None:
        try:
            import mediapipe as mp  # type: ignore

            _ = mp
        except Exception:
            return

        # We keep this minimal to avoid mandatory heavy deps in light mode.
        for subject in graph.subjects.values():
            if "person" in subject.label:
                subject.confidence = min(subject.confidence + 0.1, 1.0)


class SceneTransitionModule:
    name = "scene_transition"

    def run(self, context: AnalysisContext, graph: SceneIntelligenceGraph) -> None:
        frames = context.frames.frames_by_height[min(context.frames.frames_by_height.keys())]
        if len(frames) < 2:
            return
        try:
            import cv2  # type: ignore
        except Exception:
            return

        prev_hist = None
        for i, frame in enumerate(frames):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            hist = cv2.calcHist([gray], [0], None, [32], [0, 256])
            hist = cv2.normalize(hist, hist).flatten()
            if prev_hist is not None:
                score = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_BHATTACHARYYA)
                if score > 0.45:
                    ts = i * (graph.duration_sec / max(len(frames), 1))
                    graph.add_event(TimeEvent(ts, "scene_cut", min(1.0, score), {"score": score}))
            prev_hist = hist


class MotionModule:
    name = "motion"

    def run(self, context: AnalysisContext, graph: SceneIntelligenceGraph) -> None:
        frames = context.frames.frames_by_height[min(context.frames.frames_by_height.keys())]
        if len(frames) < 2:
            return

        try:
            import cv2  # type: ignore
        except Exception:
            return

        mags: list[float] = []
        prev = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        for frame in frames[1:]:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(prev, gray)
            mags.append(float(diff.mean()))
            prev = gray

        threshold = mean(mags) + (max(mags) - mean(mags)) * 0.4 if mags else 0
        for i, mag in enumerate(mags):
            if mag >= threshold:
                ts = (i + 1) * (graph.duration_sec / max(len(frames), 1))
                graph.add_event(TimeEvent(ts, "action_spike", min(mag / 30.0, 1.0), {"motion": mag}))


class AudioModule:
    name = "audio"

    def run(self, context: AnalysisContext, graph: SceneIntelligenceGraph) -> None:
        path = context.frames.metadata.path
        try:
            import librosa  # type: ignore
        except Exception:
            return

        try:
            y, sr = librosa.load(path, sr=None)
            _, beats = librosa.beat.beat_track(y=y, sr=sr)
            timestamps = librosa.frames_to_time(beats, sr=sr).tolist()
            for ts in timestamps:
                graph.add_event(TimeEvent(float(ts), "beat", 0.8, {}))
        except Exception:
            graph.low_confidence_warnings.append("Audio analysis failed; beat sync disabled.")


class WhisperModule:
    name = "whisper"

    def run(self, context: AnalysisContext, graph: SceneIntelligenceGraph) -> None:
        try:
            import whisper  # type: ignore
        except Exception:
            return

        try:
            model = whisper.load_model("base")
            transcript = model.transcribe(context.frames.metadata.path)
            for seg in transcript.get("segments", []):
                graph.add_event(
                    TimeEvent(float(seg["start"]), "speech", 0.75, {"text": seg.get("text", "").strip()})
                )
        except Exception:
            graph.low_confidence_warnings.append("Whisper transcription failed.")
