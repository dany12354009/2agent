from __future__ import annotations

from ..core.config import AppConfig
from ..core.licensing import LicensePolicy
from ..services.product_service import AutoCutProductService


def create_service(license_tier: str = "free") -> AutoCutProductService:
    config = AppConfig()
    policy = LicensePolicy(tier=license_tier)
    return AutoCutProductService(config=config, license_policy=policy)
