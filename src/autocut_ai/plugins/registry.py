from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class PluginRegistry:
    style_plugins: dict[str, Callable] = field(default_factory=dict)
    export_plugins: dict[str, Callable] = field(default_factory=dict)
    analysis_plugins: dict[str, Callable] = field(default_factory=dict)

    def register_style(self, name: str, factory: Callable) -> None:
        self.style_plugins[name] = factory

    def register_export(self, name: str, handler: Callable) -> None:
        self.export_plugins[name] = handler

    def register_analysis(self, name: str, module_factory: Callable) -> None:
        self.analysis_plugins[name] = module_factory
