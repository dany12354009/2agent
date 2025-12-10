"""Utilities for turning a blueprint into a working folder."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Iterable

from .blueprint import PlatformBlueprint


class PlatformScaffolder:
    """Create files and directories based on a PlatformBlueprint."""

    def __init__(self, blueprint: PlatformBlueprint) -> None:
        self.blueprint = blueprint

    def write_blueprint(self, path: Path) -> Path:
        """Persist the blueprint to a JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.blueprint.to_dict(), indent=2), encoding="utf-8")
        return path

    def scaffold(self, target_dir: Path) -> Iterable[Path]:
        """Create a directory structure for the blueprint.

        Returns an iterable of created paths.
        """
        created: list[Path] = []
        target_dir.mkdir(parents=True, exist_ok=True)

        readme_path = target_dir / "README.md"
        readme_path.write_text(self._render_readme(), encoding="utf-8")
        created.append(readme_path)

        blueprint_path = target_dir / "blueprint.json"
        self.write_blueprint(blueprint_path)
        created.append(blueprint_path)

        services_dir = target_dir / "services"
        services_dir.mkdir(exist_ok=True)
        created.append(services_dir)

        for service, description in self.blueprint.services.items():
            service_dir = services_dir / _safe_slug(service)
            service_dir.mkdir(exist_ok=True)
            created.append(service_dir)
            service_readme = service_dir / "README.md"
            service_readme.write_text(
                f"# {service}\n\n{description or 'Service details pending.'}\n",
                encoding="utf-8",
            )
            created.append(service_readme)

        return created

    def _render_readme(self) -> str:
        """Render the root README for the scaffolded platform."""
        header = f"# {self.blueprint.name}\n\n{self.blueprint.description}\n"
        features_section = self._render_list_section("Features", self.blueprint.features)
        services_section = self._render_list_section("Services", self.blueprint.services.keys())
        return "\n\n".join(filter(None, [header, features_section, services_section])) + "\n"

    @staticmethod
    def _render_list_section(title: str, items: Iterable[str]) -> str:
        items = list(items)
        if not items:
            return ""
        bullet_lines = "\n".join(f"- {item}" for item in items)
        return f"## {title}\n\n{bullet_lines}"


def _safe_slug(value: str) -> str:
    """Return a filesystem-safe slug for a service name."""
    value = value.strip().lower().replace(" ", "-")
    return "".join(ch for ch in value if ch.isalnum() or ch in {"-", "_"}) or "service"
