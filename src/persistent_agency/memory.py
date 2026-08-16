from __future__ import annotations

from dataclasses import dataclass, field

from .state import CognitiveState, Observation


@dataclass
class MemoryStore:
    short_term: list[str] = field(default_factory=list)
    persistent: list[str] = field(default_factory=list)
    long_term: list[str] = field(default_factory=list)
    consolidation_log: list[str] = field(default_factory=list)

    def write_state(self, state: CognitiveState, observations: list[Observation]) -> None:
        self.short_term.append(f"cycle={state.cycle}; foreground={state.foreground}")
        for obs in observations:
            self.short_term.append(f"observation:{obs.source}:{obs.content}")
        self.short_term = self.short_term[-32:]

    def consolidate(self) -> None:
        if not self.short_term:
            return
        summary = " | ".join(self.short_term[-8:])
        self.long_term.append(summary)
        self.consolidation_log.append(f"consolidated:{len(self.short_term)} short-term entries")
        self.short_term.clear()
