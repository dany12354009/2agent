from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TimeEvent:
    time_sec: float
    event_type: str
    confidence: float
    payload: dict


@dataclass
class SubjectState:
    subject_id: str
    label: str
    boxes: list[tuple[float, float, float, float]] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class SceneIntelligenceGraph:
    duration_sec: float
    subjects: dict[str, SubjectState] = field(default_factory=dict)
    events: list[TimeEvent] = field(default_factory=list)
    low_confidence_warnings: list[str] = field(default_factory=list)

    def add_event(self, event: TimeEvent) -> None:
        self.events.append(event)

    def upsert_subject(
        self,
        subject_id: str,
        label: str,
        confidence: float,
        box: tuple[float, float, float, float] | None = None,
    ) -> None:
        state = self.subjects.get(subject_id)
        if state is None:
            state = SubjectState(subject_id=subject_id, label=label, confidence=confidence)
            self.subjects[subject_id] = state
        state.confidence = max(state.confidence, confidence)
        if box is not None:
            state.boxes.append(box)

    def events_by_type(self, event_type: str) -> list[TimeEvent]:
        return [e for e in self.events if e.event_type == event_type]
