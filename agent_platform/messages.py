from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class Message:
    """Represents a message exchanged between agents."""

    sender: str
    receiver: Optional[str]
    content: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __str__(self) -> str:
        receiver_label = self.receiver or "broadcast"
        return f"[{self.timestamp.isoformat()}] {self.sender} -> {receiver_label}: {self.content}"
