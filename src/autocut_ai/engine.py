from __future__ import annotations

from .app.application import create_service
from .services.product_service import ProcessingResult


class AutoCutEngine:
    """Compatibility wrapper around the production service."""

    def __init__(self, license_tier: str = "free") -> None:
        self.service = create_service(license_tier=license_tier)

    def auto_edit(self, video_path: str, style: str = "clean_shorts") -> ProcessingResult:
        return self.service.process_clip(video_path, style)
