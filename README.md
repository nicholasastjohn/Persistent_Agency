# Persistent Agency

**Persistent Agency** is a research proposal and reference implementation for a three-loop cognitive architecture for artificial general intelligence. The project tests a systems hypothesis: persistent agency may benefit from heterogeneous specialist computation, continuous endogenous cognitive state, hierarchical memory, procedural automaticity, and offline consolidation operating at different timescales.

This repository does **not** claim to implement or demonstrate artificial general intelligence.

Repository: https://github.com/nicholasastjohn/Persistent_Agency

## Architecture

The architecture separates three coupled regimes:

1. **Reactive loop** - fast perception-to-action pathways that can bypass deliberation.
2. **Deliberative loop** - a recurrent Thinker plus Prompter/Router and specialist model fabric.
3. **Consolidation loop** - offline memory reorganization, skill compilation, and pathway updates.

See [`figures/three_loop_architecture_v1.2.svg`](figures/three_loop_architecture_v1.2.svg) and [`docs/ARCHITECTURE_NOTES.md`](docs/ARCHITECTURE_NOTES.md).

## Current code status

Version 0.1.0 is intentionally small. It is a deterministic architecture smoke test, not an intelligence benchmark. It demonstrates:

- cognitive-state progression with no external observation;
- human requests entering as salient environmental observations;
- scheduled operating-mode transitions;
- short-term and long-term memory interfaces;
- a consolidation transition;
- replaceable interfaces for later specialist models and tools.

## Run tests

```bash
python -m pytest
```

## Run the example

```bash
PYTHONPATH=src python examples/run_smoke_test.py
```

## Experimental foundation (`empirical-v0.2`)

The experimental branch adds typed state records, monotonic state versions,
hash-linked append-only JSONL events, captured specialist/action results, and
deterministic replay of canonical cognitive state. Existing smoke-test APIs remain
available. The three architecture conditions and model pilot are still future work.

```python
from datetime import datetime, timezone
from persistent_agency.events import EventLog, replay, state_hash
from persistent_agency.runtime import Runtime

runtime = Runtime(log_path="runs/example/events.jsonl", run_id="example")
initial = runtime.initial_state
runtime.tick(datetime.now(timezone.utc))
runtime.integrate_result("fixture-1", "recorded fixture output", datetime.now(timezone.utc))
restored = replay(initial, EventLog.read("runs/example/events.jsonl"))
assert state_hash(restored) == state_hash(runtime.state)
```

Use a fresh log path for each run; existing files are rejected rather than
overwritten or silently resumed. Preserve the initial state alongside the log
using `state_to_dict(initial)` and reconstruct it with `state_from_dict(...)`.
Replay applies the recorded state transitions without re-invoking a model, tool,
or decision policy. It restores `CognitiveState`; the legacy `MemoryStore` buffers
are not part of this replay contract yet. Captured outputs are recorded verbatim,
so use sandbox data and do not put credentials in them.

The runtime serializes its transitions within one process, checks for direct
external state mutation, and verifies the existing disk prefix before appending.
A second writer cannot open an existing run log through `EventLog`. This is a
trusted-host research trace, not tamper-proof storage or a multi-process database;
an actor able to rewrite the entire log can recompute its hashes. Hash checking
detects accidental corruption, reordered events, missing prefixes, and stale heads.
It does not detect deletion of the final complete events without an independently
retained final-state hash.

`execute_action` denies every capability by default and logs denials before
raising `PermissionError`. Explicitly allowlisted callbacks produce request and
result/failure events. A request without a later result identifies an interrupted
action; actions are never automatically retried. This callback gate is not an OS
sandbox and does not prevent arbitrary Python code outside the runtime from using
the host. No frontier-model adapter or benchmark scores are introduced here.

## Research plan

The first empirical comparison should hold model access, tool access, memory capacity, environment information, and total inference budget constant while comparing the three-loop architecture against a flatter event-triggered agent. Planned ablations include removal of endogenous cognition, consolidation, associative retrieval, procedural memory, scheduled mode switching, and specialist routing.

## Paper

The current preprint is available as:

- [`paper/Persistent_Agency_AGI_Preprint_v1.2.pdf`](paper/Persistent_Agency_AGI_Preprint_v1.2.pdf)
- [`paper/Persistent_Agency_AGI_Preprint_v1.2.docx`](paper/Persistent_Agency_AGI_Preprint_v1.2.docx)

It reports an architecture and experimental program, not experimental results.

## Safety scope

The smoke test does not perform unrestricted external actions, acquire credentials or resources, modify its own source code, or call frontier-model application programming interfaces. Human feedback is modeled as bounded priority information rather than a direct reward for acquiring compute, electrical power, money, or autonomy.

## License

No software license has been selected yet. Until one is added, third-party reuse is not affirmatively licensed.
