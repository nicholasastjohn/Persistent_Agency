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
