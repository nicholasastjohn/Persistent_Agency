from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class OperatingMode(str, Enum):
    ORIENTATION = "orientation"
    HUMAN_WORK = "human_work"
    OPEN_COGNITION = "open_cognition"
    AUTONOMOUS_COGNITION = "autonomous_cognition"
    CONSOLIDATION = "consolidation"


@dataclass(frozen=True)
class Observation:
    source: str
    content: str
    salience: float = 0.5
    is_human_request: bool = False


@dataclass(frozen=True)
class Goal:
    goal_id: str
    description: str
    priority: float = 0.0
    status: str = "active"


@dataclass(frozen=True)
class MemoryRecord:
    memory_id: str
    content: str
    creation_event_id: str
    confidence: float = 1.0
    tier: str = "short_term"
    provenance: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SpecialistRequest:
    request_id: str
    specialist: str
    prompt: str


@dataclass(frozen=True)
class ActionRequest:
    request_id: str
    capability: str
    arguments: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Procedure:
    procedure_id: str
    preconditions: list[str] = field(default_factory=list)
    action_ids: list[str] = field(default_factory=list)
    status: str = "candidate"


@dataclass
class CognitiveState:
    cycle: int = 0
    foreground: str = "initialize"
    active_goal: Optional[str] = None
    unresolved: list[str] = field(default_factory=list)
    recent_observations: list[Observation] = field(default_factory=list)
    requested_action: Optional[str] = None
    requested_specialist_work: Optional[str] = None
    operating_mode: OperatingMode = OperatingMode.ORIENTATION
    state_version: int = 0
    timestamp: Optional[str] = None
    active_goals: list[Goal] = field(default_factory=list)
    uncertainties: list[str] = field(default_factory=list)
    intentions: list[str] = field(default_factory=list)
    candidate_actions: list[ActionRequest] = field(default_factory=list)
    pending_specialist_requests: list[SpecialistRequest] = field(default_factory=list)
    recent_results: list[str] = field(default_factory=list)
    remaining_budget: Optional[float] = None

    @property
    def tick(self) -> int:
        """The original cycle counter is retained as the canonical tick counter."""
        return self.cycle

    @property
    def foreground_focus(self) -> str:
        return self.foreground
