"""Versioned, hash-linked transitions and deterministic canonical-state replay.

Replay applies recorded state transitions, including captured external results. It
does not call a model, a tool, or a potentially changed decision policy. Hashes
detect corruption; they are not signatures against an adversary rewriting a log.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, fields, is_dataclass
from datetime import datetime
from enum import Enum
import hashlib
import json
import math
import os
from pathlib import Path
from threading import RLock
import types
from typing import Any, Union, get_args, get_origin, get_type_hints

from .state import CognitiveState


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _decode(kind: Any, value: Any) -> Any:
    """Decode the declared schema without accepting booleans as integer versions."""
    origin, args = get_origin(kind), get_args(kind)
    if origin in (Union, types.UnionType):
        for option in args:
            try:
                return _decode(option, value)
            except (ValueError, TypeError):
                pass
        raise ValueError("Value does not match the state schema")
    if origin is list:
        if not isinstance(value, list):
            raise ValueError("Expected a list")
        return [_decode(args[0], item) for item in value]
    if origin is dict:
        if not isinstance(value, dict):
            raise ValueError("Expected a dictionary")
        return {_decode(args[0], key): _decode(args[1], item) for key, item in value.items()}
    if is_dataclass(kind):
        expected = {item.name for item in fields(kind)}
        if not isinstance(value, dict) or set(value) != expected:
            raise ValueError("State fields do not match the declared schema")
        hints = get_type_hints(kind)
        return kind(**{key: _decode(hints[key], item) for key, item in value.items()})
    if isinstance(kind, type) and issubclass(kind, Enum):
        return kind(value)
    if kind is float:
        if type(value) not in (int, float) or not math.isfinite(value):
            raise ValueError("Expected a finite number")
        return float(value)
    if type(value) is not kind:
        raise ValueError(f"Expected {kind}")
    return value


def state_to_dict(state: CognitiveState) -> dict[str, Any]:
    data = asdict(state)
    # A JSON round trip also normalizes string-enum values.
    data = json.loads(canonical_json(data))
    normalized = state_from_dict(data)
    return json.loads(canonical_json(asdict(normalized)))


def state_from_dict(data: dict[str, Any]) -> CognitiveState:
    state = _decode(CognitiveState, data)
    if state.state_version < 0 or state.cycle < 0:
        raise ValueError("State versions and ticks must be nonnegative")
    return state


def state_hash(state: CognitiveState) -> str:
    return _digest(state_to_dict(state))


@dataclass(frozen=True)
class Event:
    event_id: str
    run_id: str
    timestamp: str
    tick: int
    source: str
    event_type: str
    state_version_before: int
    payload: dict[str, Any]
    state_version_after: int
    parent_event_ids: list[str]
    state_hash_before: str
    state_hash_after: str
    state_after: dict[str, Any]
    previous_event_hash: str | None
    event_hash: str
    schema_version: int = 1

    def to_dict(self) -> dict[str, Any]:
        return deepcopy(asdict(self))

    @classmethod
    def create(cls, *, before: CognitiveState, after: CognitiveState, run_id: str,
               event_type: str, source: str, timestamp: str, payload: dict[str, Any],
               previous: Event | None = None) -> Event:
        values = dict(event_id=f"{run_id}:{after.state_version}", run_id=run_id,
                      timestamp=timestamp, tick=after.tick, source=source,
                      event_type=event_type, state_version_before=before.state_version,
                      payload=deepcopy(payload), state_version_after=after.state_version,
                      parent_event_ids=[previous.event_id] if previous else [],
                      state_hash_before=state_hash(before), state_hash_after=state_hash(after),
                      state_after=state_to_dict(after),
                      previous_event_hash=previous.event_hash if previous else None,
                      schema_version=1)
        return cls(**values, event_hash=_digest(values))

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Event:
        if not isinstance(data, dict) or set(data) != {item.name for item in fields(cls)}:
            raise ValueError("Event fields do not match schema version 1")
        # Payload is arbitrary JSON, but the envelope has a strict primitive schema.
        for name in ("event_id", "run_id", "timestamp", "source", "event_type",
                     "state_hash_before", "state_hash_after", "event_hash"):
            if type(data[name]) is not str or not data[name]:
                raise ValueError(f"Invalid event {name}")
        for name in ("tick", "state_version_before", "state_version_after", "schema_version"):
            if type(data[name]) is not int or data[name] < 0:
                raise ValueError(f"Invalid event {name}")
        if data["schema_version"] != 1 or not isinstance(data["payload"], dict):
            raise ValueError("Unsupported event schema or payload")
        if not isinstance(data["parent_event_ids"], list) or any(type(x) is not str for x in data["parent_event_ids"]):
            raise ValueError("Invalid parent event IDs")
        if data["previous_event_hash"] is not None and type(data["previous_event_hash"]) is not str:
            raise ValueError("Invalid previous event hash")
        datetime.fromisoformat(data["timestamp"])
        values = {key: value for key, value in data.items() if key != "event_hash"}
        if _digest(values) != data["event_hash"]:
            raise ValueError("Event hash mismatch")
        state_from_dict(data["state_after"])
        return cls(**deepcopy(data))


def replay(initial_state: CognitiveState, events: list[Event | dict[str, Any]]) -> CognitiveState:
    state = state_from_dict(state_to_dict(initial_state))
    previous: Event | None = None
    seen: set[str] = set()
    for item in events:
        event = Event.from_dict(item.to_dict() if isinstance(item, Event) else item)
        if event.event_id in seen:
            raise ValueError("Duplicate event ID")
        if previous and event.run_id != previous.run_id:
            raise ValueError("Events belong to different runs")
        if event.event_id != f"{event.run_id}:{event.state_version_after}":
            raise ValueError("Event ID does not match its run and version")
        if event.previous_event_hash != (previous.event_hash if previous else None):
            raise ValueError("Broken event hash chain")
        if event.parent_event_ids != ([previous.event_id] if previous else []):
            raise ValueError("Broken parent event chain")
        if event.state_version_before != state.state_version or event.state_version_after != state.state_version + 1:
            raise ValueError("State versions are not contiguous")
        if event.state_hash_before != state_hash(state):
            raise ValueError("Event does not apply to the current state")
        after = state_from_dict(event.state_after)
        if after.state_version != event.state_version_after or after.tick != event.tick:
            raise ValueError("Event envelope differs from recorded state")
        if after.tick < state.tick or after.timestamp != event.timestamp:
            raise ValueError("Invalid tick or timestamp transition")
        if event.state_hash_after != state_hash(after):
            raise ValueError("Recorded final state hash mismatch")
        state, previous = after, event
        seen.add(event.event_id)
    return state


class EventLog:
    """An exclusive run log. Existing files are never overwritten or resumed.

    The on-disk prefix is verified before every append. Callers receive copies,
    so changing a returned event cannot mutate the writer's history.
    """

    def __init__(self, initial_state: CognitiveState, path: str | Path | None = None):
        self._initial_state = state_from_dict(state_to_dict(initial_state))
        self.path = Path(path) if path is not None else None
        self._events: list[Event] = []
        self._bytes = b""
        self._lock = RLock()
        if self.path is not None:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            # Exclusive create prevents accidental destruction of a previous run.
            with self.path.open("xb"):
                pass

    @property
    def initial_state(self) -> CognitiveState:
        return deepcopy(self._initial_state)

    @property
    def events(self) -> list[Event]:
        with self._lock:
            return deepcopy(self._events)

    def append(self, event: Event) -> None:
        with self._lock:
            saved = deepcopy(event)
            replay(self.initial_state, self._events + [saved])
            line = (canonical_json(saved.to_dict()) + "\n").encode("utf-8")
            if self.path is not None:
                with self.path.open("r+b") as stream:
                    if stream.read() != self._bytes:
                        raise ValueError("Existing event log was changed outside its writer")
                    stream.seek(0, os.SEEK_END)
                    stream.write(line)
                    stream.flush()
                    os.fsync(stream.fileno())
            self._bytes += line
            self._events.append(saved)

    @staticmethod
    def read(path: str | Path) -> list[Event]:
        raw = Path(path).read_bytes()
        if raw and not raw.endswith(b"\n"):
            raise ValueError("Incomplete final event line")
        return [Event.from_dict(json.loads(line)) for line in raw.splitlines()]
