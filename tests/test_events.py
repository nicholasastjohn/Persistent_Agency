from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from dataclasses import replace
from datetime import datetime
import json

import pytest

from persistent_agency.events import Event, EventLog, replay, state_hash, state_to_dict
from persistent_agency.runtime import Runtime
from persistent_agency.state import (ActionRequest, CognitiveState, Goal, Observation,
                                     SpecialistRequest)


NOW = datetime(2026, 11, 1, 18)


def test_replay_reconstructs_typed_state_and_captured_outputs(tmp_path):
    initial = CognitiveState(
        active_goals=[Goal("g1", "validate replay", 0.8)],
        candidate_actions=[ActionRequest("a1", "sandbox.read", {"key": "fixture"})],
        pending_specialist_requests=[SpecialistRequest("s1", "fixture", "inspect")],
        remaining_budget=0.0,
    )
    runtime = Runtime(state=initial, log_path=tmp_path / "events.jsonl", run_id="replay-test")
    runtime.tick(NOW, [Observation("human", "inspect result", is_human_request=True)])
    runtime.integrate_result("s1", "captured external output", NOW)
    saved = EventLog.read(tmp_path / "events.jsonl")
    restored = replay(runtime.initial_state, saved)
    assert state_to_dict(restored) == state_to_dict(runtime.state)
    assert state_hash(restored) == state_hash(runtime.state)
    assert restored.recent_results == ["captured external output"]
    assert restored.pending_specialist_requests == []
    assert [item.state_version_after for item in saved] == [1, 2]
    assert restored.tick == 1  # integration versions state without inventing a Thinker tick


def test_append_preserves_prefix_and_rejects_existing_run_or_stale_event(tmp_path):
    path = tmp_path / "events.jsonl"
    runtime = Runtime(log_path=path, run_id="append-test")
    runtime.tick(NOW)
    original = path.read_bytes()
    runtime.tick(NOW)
    assert path.read_bytes().startswith(original)
    assert len(path.read_bytes().splitlines()) == 2
    with pytest.raises(FileExistsError):
        Runtime(log_path=path)
    before = path.read_bytes()
    with pytest.raises(ValueError):
        runtime._event_log.append(runtime.events[0])
    assert path.read_bytes() == before


def test_changed_disk_prefix_is_rejected_before_state_advances(tmp_path):
    path = tmp_path / "events.jsonl"
    runtime = Runtime(log_path=path)
    runtime.tick(NOW)
    old_hash = state_hash(runtime.state)
    path.write_bytes(path.read_bytes() + b"unauthorized write\n")
    with pytest.raises(ValueError, match="changed outside"):
        runtime.tick(NOW)
    assert state_hash(runtime.state) == old_hash
    assert len(runtime.events) == 1


@pytest.mark.parametrize("corruption", ["payload", "reordered", "missing", "duplicate", "version", "wrong_initial"])
def test_replay_rejects_corrupt_or_inapplicable_history(corruption):
    runtime = Runtime(run_id="integrity-test")
    runtime.tick(NOW)
    runtime.integrate_result("s1", "observed result", NOW)
    events = [item.to_dict() for item in runtime.events]
    initial = runtime.initial_state
    if corruption == "payload":
        events[1]["payload"]["result"] = "changed output"
    elif corruption == "reordered":
        events.reverse()
    elif corruption == "missing":
        events = events[1:]
    elif corruption == "duplicate":
        events.append(deepcopy(events[-1]))
    elif corruption == "version":
        events[0]["state_version_after"] = True
    else:
        initial.foreground = "different experiment"
    with pytest.raises(ValueError):
        replay(initial, events)


def test_replay_rejects_validly_hashed_noncontiguous_version():
    before = CognitiveState()
    after = replace(before, state_version=2, timestamp=NOW.isoformat())
    event = Event.create(before=before, after=after, run_id="skip", event_type="tick",
                         source="runtime", timestamp=NOW.isoformat(), payload={})
    with pytest.raises(ValueError, match="contiguous"):
        replay(before, [event])


def test_truncated_jsonl_is_rejected(tmp_path):
    path = tmp_path / "events.jsonl"
    runtime = Runtime(log_path=path)
    runtime.tick(NOW)
    path.write_bytes(path.read_bytes().rstrip(b"\n"))
    with pytest.raises(ValueError, match="Incomplete"):
        EventLog.read(path)


def test_permission_denial_logs_without_executing_action():
    runtime = Runtime()
    calls = []
    with pytest.raises(PermissionError, match="denied"):
        runtime.execute_action(ActionRequest("a1", "network.send"),
                               lambda request: calls.append(request) or "sent", NOW)
    assert calls == []
    assert [event.event_type for event in runtime.events] == ["action_denied"]
    assert runtime.state.state_version == 1
    assert runtime.state.recent_results == []
    assert state_hash(replay(runtime.initial_state, runtime.events)) == state_hash(runtime.state)


def test_explicit_capability_records_intent_and_captured_result():
    runtime = Runtime(allowed_capabilities=frozenset({"sandbox.read"}))
    result = runtime.execute_action(ActionRequest("a1", "sandbox.read"), lambda _: "fixture", NOW)
    assert result == "fixture"
    assert [event.event_type for event in runtime.events] == ["action_requested", "action_result"]
    assert replay(runtime.initial_state, runtime.events).recent_results == ["fixture"]


def test_action_failure_is_visible_and_not_retried():
    runtime = Runtime(allowed_capabilities=frozenset({"sandbox.read"}))
    calls = []

    def fail(request):
        calls.append(request)
        raise RuntimeError("fixture failure: secret credential in upstream exception")

    with pytest.raises(RuntimeError, match="fixture failure"):
        runtime.execute_action(ActionRequest("a1", "sandbox.read"), fail, NOW)
    assert len(calls) == 1
    assert [event.event_type for event in runtime.events] == ["action_requested", "action_failed"]
    assert runtime.events[-1].payload["error_type"] == "RuntimeError"
    assert "secret credential" not in json.dumps([event.to_dict() for event in runtime.events])


def test_single_writer_serializes_concurrent_integrations():
    runtime = Runtime()
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda number: runtime.integrate_result(str(number), f"result {number}", NOW), range(20)))
    assert [event.state_version_after for event in runtime.events] == list(range(1, 21))
    assert sorted(runtime.state.recent_results) == sorted(f"result {number}" for number in range(20))
    assert state_hash(replay(runtime.initial_state, runtime.events)) == state_hash(runtime.state)


def test_returned_snapshots_do_not_mutate_canonical_history():
    runtime = Runtime()
    returned = runtime.tick(NOW)
    returned.foreground = "caller change"
    events = runtime.events
    events[0].state_after["foreground"] = "caller change"
    assert runtime.state.foreground != "caller change"
    assert replay(runtime.initial_state, runtime.events).foreground == runtime.state.foreground
    runtime.state.foreground = "unsupported direct mutation"
    with pytest.raises(ValueError, match="outside the runtime"):
        runtime.tick(NOW)


def test_state_schema_rejects_nonfinite_budget_and_unknown_fields():
    from persistent_agency.events import state_from_dict
    with pytest.raises(ValueError):
        state_to_dict(CognitiveState(remaining_budget=float("nan")))
    malformed = state_to_dict(CognitiveState())
    malformed["unknown"] = "field"
    with pytest.raises(ValueError):
        state_from_dict(malformed)


def test_numeric_state_fields_have_stable_canonical_encoding():
    initial = CognitiveState(active_goals=[Goal("g1", "integer priority", 1)], remaining_budget=0)
    runtime = Runtime(state=initial)
    runtime.tick(NOW)
    assert state_hash(replay(runtime.initial_state, runtime.events)) == state_hash(runtime.state)


def test_initial_state_snapshot_cannot_change_writer_history():
    runtime = Runtime()
    snapshot = runtime.initial_state
    snapshot.foreground = "caller change"
    runtime.tick(NOW)
    assert replay(runtime.initial_state, runtime.events).foreground == runtime.state.foreground
