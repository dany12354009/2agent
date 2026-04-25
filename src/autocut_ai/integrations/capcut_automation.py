from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AutomationConfig:
    enabled: bool = False
    require_user_confirmation: bool = True
    dry_run: bool = True


class CapCutCompanion:
    """Step-by-step import guide for manual CapCut workflow."""

    def build_steps(self, export_paths: dict[str, str]) -> list[str]:
        return [
            "Open CapCut and create a new project.",
            "Import the source video clip.",
            f"Load timeline helper JSON: {export_paths.get('timeline_json', '')}",
            f"Apply keyframe points from CSV: {export_paths.get('keyframes_csv', '')}",
            f"Import captions (optional): {export_paths.get('captions_srt', '')}",
            f"Review effect recommendations: {export_paths.get('effects_json', '')}",
        ]


class CapCutAutomation:
    """Optional UI automation layer with safety confirmation and dry-run mode."""

    def __init__(self, config: AutomationConfig | None = None) -> None:
        self.config = config or AutomationConfig()

    def apply_plan(self, timeline_json_path: str, approved: bool = False) -> str:
        if not self.config.enabled:
            return "Automation disabled. Use Export/Companion modes."
        if self.config.require_user_confirmation and not approved:
            return "Automation blocked: user confirmation required."
        if self.config.dry_run:
            return f"Dry-run: would apply timeline from {timeline_json_path}"

        try:
            import pyautogui  # type: ignore
        except Exception:
            return "pyautogui is unavailable, cannot run live automation."

        pyautogui.alert(text=f"Applying timeline: {timeline_json_path}", title="AutoCut AI", button="Continue")
        return "Automation completed."
