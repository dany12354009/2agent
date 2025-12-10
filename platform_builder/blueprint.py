"""Blueprint model for describing new platforms."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class PlatformBlueprint:
    """In-memory description of a platform configuration.

    A blueprint captures the essential information required to scaffold
    a new platform: its name, a short description, the features it should
    offer, and the services that power it.
    """

    name: str
    description: str
    features: List[str] = field(default_factory=list)
    services: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        self.description = self.description.strip()
        if not self.name:
            raise ValueError("Platform name cannot be empty.")
        if not self.description:
            raise ValueError("Platform description cannot be empty.")
        self.features = [feature.strip() for feature in self.features if feature.strip()]
        self.services = {k.strip(): v.strip() for k, v in self.services.items() if k.strip()}

    def to_dict(self) -> Dict[str, object]:
        """Return a serialisable dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "features": list(self.features),
            "services": dict(self.services),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "PlatformBlueprint":
        """Create a blueprint from a mapping."""
        name = str(data.get("name", "")).strip()
        description = str(data.get("description", "")).strip()
        features_raw = data.get("features")
        services_raw = data.get("services")

        features: List[str]
        if isinstance(features_raw, list):
            features = [str(item) for item in features_raw]
        elif features_raw is None:
            features = []
        else:
            raise TypeError("features must be a list of strings")

        services: Dict[str, str]
        if isinstance(services_raw, dict):
            services = {str(k): str(v) for k, v in services_raw.items()}
        elif services_raw is None:
            services = {}
        else:
            raise TypeError("services must be a mapping of service name to summary")

        return cls(name=name, description=description, features=features, services=services)

    def summary(self) -> str:
        """Return a human-friendly summary of the blueprint."""
        lines = [f"Platform: {self.name}", f"Description: {self.description}"]
        if self.features:
            lines.append("Features:")
            lines.extend([f"- {feature}" for feature in self.features])
        if self.services:
            lines.append("Services:")
            lines.extend([f"- {name}: {details}" for name, details in self.services.items()])
        return "\n".join(lines)
