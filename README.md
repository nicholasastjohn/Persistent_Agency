# Persistent Agency

**Persistent Agency** is a research proposal and reference implementation for a three-loop cognitive architecture for autonomous general intelligence. The project tests a systems hypothesis: persistent agency may benefit from heterogeneous specialist computation, continuous endogenous cognitive state, hierarchical memory, procedural automaticity, and offline consolidation operating at different timescales.

This repository does **not** claim to implement or demonstrate artificial general intelligence.

## Architecture

The architecture separates three coupled regimes:

1. **Reactive loop** - fast perception-to-action pathways that can bypass deliberation.
2. **Deliberative loop** - a recurrent Thinker plus Prompter/Router and specialist model fabric.
3. **Consolidation loop** - offline memory reorganization, skill compilation, and pathway updates.

See [`figures/three_loop_architecture_v1.1.svg`](figures/three_loop_architecture_v1.1.svg) and [`docs/ARCHITECTURE_NOTES.md`](docs/ARCHITECTURE_NOTES.md).

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

## Research plan

The first empirical comparison should hold model access, tool access, memory capacity, environment information, and total inference budget as constant while comparing the three-loop architecture against a flatter event-triggered agent. Planned ablations include removal of endogenous cognition, consolidation, associative retrieval, procedural memory, scheduled mode switching, and specialist routing.

## Paper

The current preprint is in `paper/` as Word and PDF files. It reports an architecture and experimental program, not experimental results.

## Safety scope

The smoke test does not perform unrestricted external actions, acquire credentials or resources, modify its own source code, or call frontier-model APIs. Human feedback is modeled as bounded priority information rather than a direct reward for acquiring compute, electrical power, money, or autonomy.

## License

No license has been selected yet. Add one before inviting third-party reuse or contributions.
