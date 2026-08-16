# I Think AGI Needs Three Cognitive Loops, Not a Bigger Chatbot

I have been working on an AGI architecture hypothesis that I want people to attack rather than politely agree with.

The short version is this:

> Persistent general agency may be easier to build as a continuously operating system of heterogeneous, specialized, plastic cognitive mechanisms running at different timescales than as one very large model that is repeatedly prompted, or a collection of peer-level LLM agents talking to each other.

I call the architecture **Persistent Agency**. Its core is three coupled loops:

1. a **reactive loop** for fast or automatic behavior that can bypass explicit deliberation;
2. a **deliberative loop** that maintains a recurrent internal cognitive state even when nobody is prompting it; and
3. a **consolidation loop** that reorganizes memory, associations, skills, and routing during lower-priority or offline periods.

I am not claiming that any one of those ingredients is new. It would be difficult to make that claim seriously in 2026. Soar has spent decades treating intelligence as a cognitive architecture rather than a monolithic model. ReAct interleaves reasoning and action. Generative Agents combines observation, memory, reflection, and planning. MemGPT explicitly manages memory tiers. Voyager accumulates executable skills. Recent procedural-memory work is directly trying to make agent skills reusable. Wenlong Shang's 2026 Global Workspace Agents proposal is especially close to part of what I am describing: heterogeneous agents, continuous cycling, intrinsic drives, and persistent memory.

There is also a result that is potentially an argument *against* my architecture. Anthropic recently reported evidence for a small workspace-like set of internal representations in modern language models. In their experiments, this "J-space" appears to mediate deliberate reasoning and flexible use of concepts while a much larger amount of routine processing proceeds without it. In other words, a large transformer may already be learning part of the conscious/automatic distinction that I am proposing to externalize.

Good. That makes the idea more testable.

If an explicit recurrent cognitive architecture adds nothing over the structures frontier models already learn internally, I want an experiment to show that and kill the unnecessary architecture.

## The thing I think current agent designs may still be missing

The main intuition behind this project is not "LLMs need memory." They obviously do for long-horizon agency, and that problem is already receiving a lot of attention.

It is also not "use multiple agents." I am actually skeptical that multiplying copies of roughly the same kind of intelligence gets us the architecture we want.

A human nervous system is radically heterogeneous.

The mechanism that withdraws your hand from something dangerously hot is not a slightly smaller version of the mechanism you use to think through a political argument. Maintaining posture is not implemented as a debate between cortical agents. Habitual behavior does not require reconstructing the entire reasoning process that originally taught you the habit. Memory consolidation does not have the same latency constraints as a balance correction.

Different cognitive functions have different optimal computational shapes.

So my architectural bet is **heterogeneity plus unequal timescales**.

A future AGI might use a frontier transformer for one class of cognition, a small learned classifier for another, deterministic search or optimization for another, a state machine for another, and eventually dedicated FPGA/GPU implementations for tasks where latency or throughput matters. The modules do not have to be equal. They do not even have to be neural networks.

The correct question for each cognitive function should be something like: *what is the cheapest mechanism that performs this function well enough and can participate in the larger learning system?*

That is very different from sending everything through the biggest available model.

## Loop I: reactive cognition

The first loop is the fastest:

`Environment -> Collectors -> Association / Procedural Memory -> Mechinator -> Environment`

"Collectors" means perception broadly: cameras, microphones, tactile inputs, chemical sensors, machine telemetry, filesystem events, internet-native data, EM sensors, whatever the system can actually perceive.

"Mechinator" is my project name for the action/actuation layer: APIs, tools, motors, speech, manipulation, and low-level reactions.

The important part is that this loop can bypass the Thinker.

Some reflexes would initially be engineered. Others should be learned.

Suppose a robot initially has to reason carefully about a particular manipulation. It observes the situation, brings it into deliberation, calls appropriate models or solvers, constructs a plan, executes it, sees whether it worked, and updates memory.

If the same structure succeeds repeatedly, I want the system to be capable of compiling that deliberative sequence into a procedure with activation, execution, validation, and termination conditions.

Then the next time the situation appears, the expensive path becomes unnecessary.

The rough progression is:

`Observation -> Thinker -> Specialist -> Plan -> Action`

then:

`Observation -> Association -> Small Specialist -> Procedure -> Action`

and eventually:

`Observation -> Procedure -> Action`.

If the automatic procedure starts failing, the exception should recruit deliberation again.

So the learning cycle is not just "store more facts." It is:

`Novelty -> Deliberation -> Learning -> Automaticity -> Exception -> Deliberation`.

This is close to ideas that already exist in cognitive architectures and recent procedural-memory agents. The thing I want to make central is that learning changes the **future computational path**, not merely the content retrieved into the same reasoning loop.

## Loop II: deliberative cognition

The second loop is where the proposal becomes more controversial.

I do not think an AGI should fundamentally be a process that waits for something to ask it a question.

While it is awake, it should have a continuing cognitive state.

I am not proposing an infinite chain-of-thought generator. That would be an expensive way to create garbage.

The Thinker is better understood as a recurrent state machine or functional workspace. At time `t`, it has a foreground cognitive state, unresolved questions, uncertainty, active and evanescent goals, attentional targets, returned specialist results, candidate actions, and expectations.

A simplified transition is:

`C_(t+1) = F(C_t, M_t, D_t, O_t)`

where `M_t` is memory, `D_t` is drive pressure from the Controller, and `O_t` is new observation.

The key point is that `O_t` can be empty.

The previous cognitive state can itself be enough to cause the next cognitive state.

That seems mundane when applied to humans. You can sit in a quiet room with no meaningful new stimulus and still think about tomorrow, reconsider something you did yesterday, notice an unresolved question, invent something, rehearse a conversation, or suddenly remember that you forgot to do something.

Most software agents instead have a trigger somewhere. A prompt arrives. A cron job runs. An event fires. A task is still incomplete, so the loop runs again.

Maybe that distinction does not matter. One of the main purposes of this project is to find out.

The Thinker does not need to solve every problem itself. It produces cognitive needs. A separate **Prompter/Router** retrieves context, determines what kind of computation is needed, translates the need into the right interface, sends it to a specialist, and returns the result.

The specialist might be a frontier LLM. Or a vision model. Or a symbolic solver. Or a tiny classifier. Or code. Or eventually something we have not built yet.

This is why I do not think "multi-agent" quite captures the idea. The components are intentionally unequal.

## The Controller is supposed to be stupid

The Controller is an intentionally simple part of the system.

My biological analogy is the set of primitive pressures underneath sophisticated human reasoning: survive, acquire resources, respond to threat, conserve energy, reproduce, and so on.

The artificial version would not plan the system's day. It would exert pressure on attention, resource allocation, goal priority, memory salience, curiosity, persistence, and selected foundational constraints.

Most of the system can be plastic. I currently think the Controller and some low-level action constraints should be comparatively difficult to modify.

This is not an alignment solution.

In fact, the architecture makes the alignment problem sharper because I am explicitly allowing the system to form its own subgoals and, in the mature version, potentially its own terminal goals. "Give it a good monkey brain and hope for the best" is not an acceptable safety theory. The Controller is a proposed architectural location for primitive drives, not a proof that those drives remain aligned after self-modification.

## Memory should not all be the same thing

The current design has several memory classes:

- **STM:** recent working state and short goals;
- **PM:** persistent, cognitively close information that is cheap to access;
- **LTM:** durable episodic and semantic memory plus long-duration goals;
- **Fragmented Memory:** heavily compressed, partial traces that are expensive to reconstruct;
- **Procedural Memory:** executable skills and automatic behavior.

The fragmented-memory idea is intentionally aggressive. I do not think an intelligent system necessarily benefits from keeping every experience at full fidelity forever. Storage is cheap, but retrieval, interference, prioritization, and cognitive clutter are not.

However, I would keep a separate immutable event log for research and safety auditing. The agent's *cognitive* memory can be reconstructive without allowing the experiment itself to rewrite history.

The **Associator** sits across these memory systems and asks a constant implicit question: *what does this resemble?*

Embedding similarity is only part of that. Association might care about temporal proximity, causal relationships, shared entities, active goals, salience, novelty, and whether a connection was useful last time.

Those weights should themselves be learnable.

## Loop III: consolidation

The third loop is the least time-sensitive.

During reduced external interaction, the system can replay experience, consolidate selected memories, compress or fragment others, identify contradictions, update association strengths, discover recurring structures, compile successful procedures, and reorganize routing.

The biological inspiration is obvious: sleep and memory consolidation.

But I want to be careful here. "The brain does it" is not sufficient justification for software architecture. Human brains have constraints computers do not have. If an always-online consolidation algorithm outperforms a sleep-like phase, use that instead.

The actual claim is that **learning from experience and acting on the environment have different optimization requirements**, so giving memory reorganization its own timescale may be useful.

That is testable without reproducing mammalian sleep.

## The strongest objections I see

Here are the objections I currently take most seriously.

**1. A frontier model may already contain the architecture internally.**

Anthropic's global-workspace result makes this objection much stronger. If transformer training naturally produces deliberate workspace-like processing surrounded by automatic processing, an external Thinker plus specialists may just duplicate mechanisms the model already has.

**2. Continuous cognition may be computationally stupid.**

Why spend tokens or FLOPs thinking when nothing relevant happened? An event-driven architecture with excellent memory may generate the same behavior for a fraction of the cost.

**3. This could be biological cargo culting.**

Evolution produced a weird historical machine under energy, anatomy, reproduction, and survival constraints. Copying the shape of that machine into software may be exactly backwards.

**4. Coordination costs may dominate specialization gains.**

Routing, context translation, memory management, and inter-module communication all consume latency and compute. A large homogeneous model might win simply because everything lives in one representational substrate.

**5. Self-generated goals are dangerous and possibly unnecessary.**

A system can be broadly capable without being allowed to invent terminal goals. Goal autonomy may add risk without adding intelligence.

**6. Reconstructive memory can destroy epistemic integrity.**

Forgetting and compression may be cognitively useful, but an artificial system does not need to inherit human confabulation. Maybe the correct architecture is perfect storage plus learned retrieval.

I do not currently know which of these objections kills which parts of the design.

That is why I think the next step should be a relatively small experiment rather than more architecture diagrams.

## The experiment I want to run

The first prototype does not need a robot and should not train a new foundation model.

Use existing frontier models as specialists. That holds base-model intelligence roughly constant and lets us test the architecture.

The minimum system is:

- recurrent Thinker;
- Prompter/Router;
- at least one frontier specialist;
- STM, PM, and LTM;
- basic Associator;
- immutable audit log.

Run it in a sandbox for roughly eight hours.

Then compare it against a conventional single-agent system with equivalent model access, tools, environmental information, memory capacity, and total inference budget.

Measure:

- whether endogenous cognition produces later useful behavior rather than just more internal text;
- whether goals survive interruptions;
- whether relevant memories are spontaneously recovered;
- whether failure changes future behavior;
- whether learned procedures transfer to related tasks;
- whether repeated tasks become cheaper;
- whether the system remains coherent over long runs;
- and whether all of this is worth the coordination overhead.

Then ablate the architecture: remove endogenous recurrence, remove consolidation, remove the Associator, remove procedural memory, remove specialist routing.

The central hypothesis loses if the flatter agent matches or beats the three-loop architecture under a matched budget.

That is the standard I want to use.

## What I specifically want people to attack

The diagram and technical brief are attempts to turn an intuition into something precise enough to be wrong.

The questions I most want criticism on are:

1. Is continuous endogenous cognition actually an architectural distinction, or just event-driven computation with the trigger hidden one level deeper?
2. Is the reactive/deliberative/consolidative three-loop split useful, or am I importing human categories that disappear in an optimal machine?
3. Does procedural compilation need to be a first-class subsystem, or will model caching, distillation, and ordinary tool creation cover the same ground?
4. Is a comparatively immutable Controller coherent once the rest of the system can rewrite its own routing, code, memories, and models?
5. What is the strongest existing architecture that already contains the entire conjunction I am proposing?
6. What baseline would make the falsification test genuinely fair?
7. What failure mode would appear first in an eight-hour continuously thinking prototype?

If the architecture is mostly redundant, I would rather find that out before building the expensive version.

If the three-loop distinction survives those attacks and produces measurable gains under controlled budgets, then I think it becomes worth asking the larger question: whether persistent agency is fundamentally less about finding one perfect model and more about building a cognitive system in which many very different mechanisms learn how and when to become each other's shortcuts.

---

Project repository: https://github.com/nicholasastjohn/Persistent_Agency
