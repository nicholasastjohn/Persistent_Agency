from __future__ import annotations

from .state import CognitiveState, Observation


class Associator:
    """Very small placeholder for salience and association routing."""

    def activate(self, state: CognitiveState, observations: list[Observation]) -> list[Observation]:
        # Human requests are highly salient in this prototype, but the bounded
        # priority does not grant resources or bypass safety constraints.
        return sorted(
            observations,
            key=lambda o: (o.is_human_request, o.salience),
            reverse=True,
        )
