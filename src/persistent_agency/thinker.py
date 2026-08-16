from __future__ import annotations

from copy import deepcopy

from .state import CognitiveState, Observation, OperatingMode


class Thinker:
    """Deterministic recurrent state machine used only as an architecture smoke test."""

    def step(
        self,
        state: CognitiveState,
        salient: list[Observation],
        goals: list[str],
        operating_mode: OperatingMode,
    ) -> CognitiveState:
        nxt = deepcopy(state)
        nxt.cycle += 1
        nxt.operating_mode = operating_mode
        nxt.recent_observations = salient[:5]
        nxt.requested_action = None
        nxt.requested_specialist_work = None

        human = next((o for o in salient if o.is_human_request), None)
        if human is not None and operating_mode != OperatingMode.CONSOLIDATION:
            nxt.foreground = f"answer human request: {human.content}"
            nxt.requested_specialist_work = human.content
            nxt.requested_action = "respond_to_human"
            return nxt

        if operating_mode == OperatingMode.CONSOLIDATION:
            nxt.foreground = "audit recent work and consolidate memory"
            return nxt

        if goals:
            goal = state.active_goal or goals[0]
            nxt.active_goal = goal
            nxt.foreground = f"advance goal: {goal}"
            nxt.requested_specialist_work = f"next useful step for goal: {goal}"
            return nxt

        # Critical property: cognition still advances with no external stimulus.
        nxt.foreground = f"endogenous reflection after cycle {state.cycle}: inspect unresolved state"
        return nxt

    def integrate(self, state: CognitiveState, specialist_result: str) -> CognitiveState:
        nxt = deepcopy(state)
        nxt.foreground = f"integrate specialist result: {specialist_result}"
        return nxt
