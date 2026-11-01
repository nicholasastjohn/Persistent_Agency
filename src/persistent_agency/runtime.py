from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from threading import RLock
from typing import Callable
from uuid import uuid4

from .associator import Associator
from .memory import MemoryStore
from .events import Event, EventLog, state_hash
from .schedule import CircadianSchedule
from .state import ActionRequest, CognitiveState, Observation, OperatingMode
from .thinker import Thinker


@dataclass
class Runtime:
    thinker: Thinker = field(default_factory=Thinker)
    associator: Associator = field(default_factory=Associator)
    memory: MemoryStore = field(default_factory=MemoryStore)
    schedule: CircadianSchedule = field(default_factory=CircadianSchedule)
    state: CognitiveState = field(default_factory=CognitiveState)
    goals: list[str] = field(default_factory=list)
    log_path: str | Path | None = None
    run_id: str = field(default_factory=lambda: str(uuid4()))
    allowed_capabilities: frozenset[str] = field(default_factory=frozenset)
    _lock: RLock = field(default_factory=RLock, init=False, repr=False)
    _event_log: EventLog = field(init=False, repr=False)
    _expected_hash: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.state = deepcopy(self.state)
        self.allowed_capabilities = frozenset(self.allowed_capabilities)
        self._event_log = EventLog(self.state, self.log_path)
        self._expected_hash = state_hash(self.state)

    @property
    def events(self) -> list[Event]:
        return self._event_log.events

    @property
    def initial_state(self) -> CognitiveState:
        return deepcopy(self._event_log.initial_state)

    def _check_state(self) -> None:
        if state_hash(self.state) != self._expected_hash:
            raise ValueError("Canonical state was modified outside the runtime writer")

    def _commit(self, after: CognitiveState, now: datetime, event_type: str,
                payload: dict, source: str = "runtime") -> CognitiveState:
        self._check_state()
        after.state_version = self.state.state_version + 1
        after.timestamp = now.isoformat()
        previous = self._event_log.events
        event = Event.create(before=self.state, after=after, run_id=self.run_id,
                             event_type=event_type, source=source,
                             timestamp=after.timestamp, payload=payload,
                             previous=previous[-1] if previous else None)
        # Persist the event before publishing the new canonical state.
        self._event_log.append(event)
        self.state = deepcopy(after)
        self._expected_hash = state_hash(self.state)
        return deepcopy(self.state)

    def tick(self, now: datetime, observations: list[Observation] | None = None) -> CognitiveState:
        with self._lock:
            self._check_state()
            observations = deepcopy(observations or [])
            mode = self.schedule.mode_at(now)
            salient = self.associator.activate(deepcopy(self.state), observations)
            after = self.thinker.step(deepcopy(self.state), salient, list(self.goals), mode)
            result = self._commit(after, now, "thinker_tick", {
                "observations": [vars(obs) for obs in observations],
                "goals": list(self.goals), "operating_mode": mode.value,
            })
            self.memory.write_state(self.state, observations)
            if mode == OperatingMode.CONSOLIDATION:
                self.memory.consolidate()
            return result

    def integrate_result(self, request_id: str, result: str, now: datetime) -> CognitiveState:
        """Integrate a captured specialist output through the sole state writer."""
        with self._lock:
            self._check_state()
            if not isinstance(request_id, str) or not request_id or not isinstance(result, str):
                raise ValueError("A request ID and text result are required")
            after = self.thinker.integrate(deepcopy(self.state), result)
            after.recent_results.append(result)
            after.pending_specialist_requests = [
                item for item in after.pending_specialist_requests if item.request_id != request_id
            ]
            return self._commit(after, now, "specialist_result", {
                "request_id": request_id, "result": result,
            }, source="specialist")

    def execute_action(self, request: ActionRequest, executor: Callable[[ActionRequest], str],
                       now: datetime) -> str:
        """Gate explicitly supplied callbacks; this is not an operating-system sandbox."""
        with self._lock:
            self._check_state()
            if (not isinstance(request, ActionRequest) or not request.request_id
                    or not isinstance(request.request_id, str)
                    or not isinstance(request.capability, str) or not request.capability
                    or not isinstance(request.arguments, dict)
                    or any(not isinstance(key, str) or not isinstance(value, str)
                           for key, value in request.arguments.items())):
                raise ValueError("A typed action request with text arguments is required")
            payload = {"request_id": request.request_id, "capability": request.capability,
                       "arguments": deepcopy(request.arguments)}
            if request.capability not in self.allowed_capabilities:
                self._commit(deepcopy(self.state), now, "action_denied", payload)
                raise PermissionError(f"Capability denied: {request.capability}")
            # Log intent before invoking an external callback. A crash between the
            # request and result is deliberately visible, not silently retried.
            self._commit(deepcopy(self.state), now, "action_requested", payload)
            try:
                result = executor(deepcopy(request))
                if not isinstance(result, str):
                    raise TypeError("Action callbacks must return text")
            except Exception as error:
                self._commit(deepcopy(self.state), now, "action_failed", {
                    **payload, "error_type": type(error).__name__,
                })
                raise
            after = deepcopy(self.state)
            after.recent_results.append(result)
            self._commit(after, now, "action_result", {**payload, "result": result})
            return result
