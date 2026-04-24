from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AutomationConfig:
    enabled: bool = False
    require_user_confirmation: bool = True


class CapCutAutomation:
    """Optional UI automation module.

    Disabled by default for safety. Uses pyautogui only when user explicitly enables it.
    """

    def __init__(self, config: AutomationConfig | None = None) -> None:
        self.config = config or AutomationConfig()

    def apply_plan(self, timeline_json_path: str) -> str:
        if not self.config.enabled:
            return "Automation disabled. Exported files are ready for manual CapCut import."

        try:
            import pyautogui  # type: ignore
        except Exception:
            return "Automation requested but pyautogui is unavailable."

        # Prototype placeholder: concrete selectors/hotkeys vary by OS and CapCut version.
        pyautogui.alert(
            text=f"Load timeline manually from: {timeline_json_path}",
            title="AutoCut AI",
            button="OK",
        )
        return "Automation prompt shown."
