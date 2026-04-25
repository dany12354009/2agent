from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LicensePolicy:
    tier: str = "free"

    def allow_style(self, style: str) -> bool:
        if self.tier == "pro":
            return True
        return style in {"clean_shorts", "gaming_short", "cinematic"}

    def max_export_height(self) -> int:
        return 1920 if self.tier == "pro" else 1080

    def watermark_required(self) -> bool:
        return self.tier == "free"
