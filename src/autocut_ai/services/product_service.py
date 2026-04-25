from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..analysis.pipeline import AnalysisPipeline
from ..core.config import AppConfig
from ..core.licensing import LicensePolicy
from ..decision.engine import DecisionEngine
from ..exporters.capcut_exports import (
    export_effect_recommendations,
    export_keyframes_csv,
    export_timeline_json,
)
from ..exporters.subtitles import export_srt
from ..models import EditPlan
from ..timeline.generator import TimelineGenerator, TimelineProject
from ..video.engine import VideoProcessingEngine


@dataclass
class ProcessingResult:
    plan: EditPlan
    timeline: TimelineProject
    warnings: list[str]


class AutoCutProductService:
    def __init__(self, config: AppConfig | None = None, license_policy: LicensePolicy | None = None) -> None:
        self.config = config or AppConfig()
        self.license_policy = license_policy or LicensePolicy()
        self.video_engine = VideoProcessingEngine()
        self.analysis = AnalysisPipeline(self.config)
        self.timeline_generator = TimelineGenerator()

    def process_clip(self, video_path: str, style_name: str) -> ProcessingResult:
        if not self.license_policy.allow_style(style_name):
            raise PermissionError(f"Style '{style_name}' requires Pro license")

        frames = self.video_engine.extract_frames(video_path, heights=[360, 720], sample_fps=6.0)
        graph = self.analysis.run(frames)
        decisions = DecisionEngine(style_name=style_name, intensity=self.config.product.edit_intensity)
        actions = decisions.build_actions(graph)
        plan = EditPlan(source_video=video_path, style=style_name, actions=actions)
        timeline = self.timeline_generator.build(plan, frames.metadata.duration_sec)
        return ProcessingResult(plan=plan, timeline=timeline, warnings=graph.low_confidence_warnings)

    def batch_process(self, videos: list[str], style_name: str) -> list[ProcessingResult]:
        return [self.process_clip(path, style_name) for path in videos]

    def export_all(self, result: ProcessingResult, out_dir: str) -> dict[str, str]:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        timeline_path = export_timeline_json(result.plan, out / "timeline.json")
        keyframes_path = export_keyframes_csv(result.plan, out / "keyframes.csv")
        effects_path = export_effect_recommendations(result.plan, out / "effects.json")

        speech = [a for a in result.plan.actions if a.effect == "text_caption"]
        captions = [(a.timestamp, a.timestamp + 1.5, a.reason.replace("Speech transcription for caption: ", "")) for a in speech]
        srt_path = export_srt(captions, out / "captions.srt") if captions else None

        return {
            "timeline_json": str(timeline_path),
            "keyframes_csv": str(keyframes_path),
            "effects_json": str(effects_path),
            "captions_srt": str(srt_path) if srt_path else "",
        }
