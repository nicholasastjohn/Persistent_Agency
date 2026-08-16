from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from .associator import Associator
from .memory import MemoryStore
from .schedule import CircadianSchedule
from .state import CognitiveState, Observation, OperatingMode
from .thinker import Thinker


@dataclass
class Runtime:
    thinker: Thinker = field(default_factory=Thinker)
    associator: Associator = field(default_factory=Associator)
    memory: MemoryStore = field(default_factory=MemoryStore)
    schedule: CircadianSchedule = field(default_factory=CircadianSchedule)
    state: CognitiveState = field(default_factory=CognitiveState)
    goals: list[str] = field(default_factory=list)

    def tick(self, now: datetime, observations: list[Observation] | None = None) -> CognitiveState:
        observations = observations or []
        mode = self.schedule.mode_at(now)
        salient = self.associator.activate(self.state, observations)
        self.state = self.thinker.step(self.state, salient, self.goals, mode)
        self.memory.write_state(self.state, observations)
        if mode == OperatingMode.CONSOLIDATION:
            self.memory.consolidate()
        return self.state
