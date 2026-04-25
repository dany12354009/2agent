from __future__ import annotations

from dataclasses import dataclass

from ..services.product_service import ProcessingResult


@dataclass
class TUIViewModel:
    video_path: str = ""
    style: str = "clean_shorts"
    intensity: float = 0.7
    output_dir: str = "autocut_output"
    status: str = "Press i to input video, s to change style, r to run"


def render_header(model: TUIViewModel) -> list[str]:
    return [
        "AutoCut AI TUI",
        f"Video: {model.video_path or '(none)'}",
        f"Style: {model.style} | Intensity: {model.intensity:.2f} | Out: {model.output_dir}",
        f"Status: {model.status}",
    ]


def render_result_lines(result: ProcessingResult | None, max_items: int = 12) -> list[str]:
    if result is None:
        return ["No analysis yet."]

    lines = ["Suggested actions:"]
    for action in result.plan.actions[:max_items]:
        lines.append(
            f"- {action.timestamp:6.2f}s [{action.effect:<12}] target={action.tracking_target} "
            f"intensity={action.intensity:.2f}"
        )

    if result.warnings:
        lines.append("")
        lines.append("Warnings:")
        lines.extend(f"! {warning}" for warning in result.warnings[:5])
    return lines
