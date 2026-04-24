from __future__ import annotations

from .analyzers.audio import AudioBeatAnalyzer
from .analyzers.motion import MotionIntensityAnalyzer
from .analyzers.scene import SceneChangeAnalyzer
from .analyzers.subject import SubjectAnalyzer
from .analyzers.video_loader import load_video
from .models import AnalysisResult, EditPlan, EditStyle
from .planner import EditPlanner


class AutoCutEngine:
    """Pipeline coordinator: load video -> analyze -> create edit plan."""

    def __init__(self) -> None:
        self.scene = SceneChangeAnalyzer()
        self.motion = MotionIntensityAnalyzer()
        self.audio = AudioBeatAnalyzer()
        self.subject = SubjectAnalyzer()
        self.planner = EditPlanner()

    def analyze(self, video_path: str) -> AnalysisResult:
        metadata, frames = load_video(video_path)
        scene_data = self.scene.run(metadata, frames)
        motion_data = self.motion.run(metadata, frames)
        audio_data = self.audio.run(metadata, frames)
        subject_data = self.subject.run(metadata, frames)

        return AnalysisResult(
            duration_sec=metadata.duration_sec,
            scene_cuts=scene_data["scene_cuts"],
            beat_timestamps=audio_data["beat_timestamps"],
            motion_spikes=motion_data["motion_spikes"],
            detected_subjects=subject_data["detected_subjects"],
            main_subject_id=subject_data["main_subject_id"],
        )

    def auto_edit(self, video_path: str, style: EditStyle) -> EditPlan:
        analysis = self.analyze(video_path)
        return self.planner.build(video_path, style, analysis)
