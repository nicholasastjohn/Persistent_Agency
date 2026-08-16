# Architecture Notes

## Core hypothesis

Persistent general agency may be better supported by continuously operating, heterogeneous, specialized, and plastic cognitive subsystems interacting across multiple timescales than by repeatedly invoking a flatter homogeneous reasoning system only when externally prompted.

## The three loops

### Loop I - Reactive

`Environment -> Collectors -> Associator / Procedural Memory -> Mechinator -> Environment`

The reactive path is intentionally allowed to bypass the Thinker. Initially it may contain engineered policies; repeated successful deliberative behavior may later be compiled into procedural pathways.

### Loop II - Deliberative

`Thinker -> Prompter/Router -> Specialists/Tools -> Memory/Association -> Thinker -> Action -> Observation -> Thinker`

The Thinker is a recurrent cognitive-state process. External input is optional. Its previous state can cause the next state.

### Loop III - Consolidation

During low-interaction periods the system audits recent work, reorganizes memory, prunes or fragments low-value information, discovers associations, and compiles reusable procedures.

## Controller

The Controller is deliberately simple and relatively resistant to self-modification. It applies persistent pressure to attention, goals, resource budgeting, and safety constraints. Human requests arrive through Collectors. A bounded human-responsiveness pressure can prioritize cooperation, but resource acquisition itself should not be a reward signal.

## Circadian operating policy

The prototype schedule is a **harness policy**, not a core cognitive law:

- 07:00-08:00 - orientation and planning
- 08:00-12:00 - human-facing work; interruptible
- 12:00-13:00 - open cognition
- 13:00-17:00 - human-facing work; interruptible
- 17:00-21:00 - autonomous cognition
- 21:00-07:00 - consolidation and system audit

The schedule changes priorities and resource allocation. It should not generate the next thought. The recurrent Thinker continues within every active mode.

## Memory hierarchy

- Short-Term Memory: recent working state.
- Persistent Memory: durable, high-availability state.
- Long-Term Memory: consolidated episodic and semantic information.
- Fragmented Memory: compressed, lossy, expensive-to-recover traces.
- Procedural Memory: reusable executable skills and automatic pathways.

## First experimental question

Under matched model and inference budgets, does persistent recurrence plus memory and mode management improve useful long-horizon behavior relative to an event-triggered baseline?

The repository's current tests validate only software mechanics. They do not answer this scientific question.
