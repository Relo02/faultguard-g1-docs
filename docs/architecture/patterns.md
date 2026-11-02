# Styles and patterns

!!! baseline "Baseline"
    The styles and patterns are named in the proposal §5. The *how* is proposed. Each is written as what, why and how, ready to adapt for Design Document §2D.

## Styles

### Event-driven, publish-subscribe

**What.** Components interact only by publishing immutable events to typed topics and subscribing to the topics they need.

**Why.** It is what lets a new check be added without changing existing components (NFR11). It also isolates failures and overload to one consumer, and makes the whole system observable, because the log simply subscribes to everything.

**How.** `EventBus` with one bounded queue per subscription. See [Event bus](../design/event-bus.md).

### Pipes and filters, within the events

**What.** Telemetry flows through stages that each transform their input into a new kind of output: sample → window → evidence → fused score → hypothesis → state.

**Why.** Each stage can be understood and tested alone, using recorded events as input.

**How.** Each stage is a class with handler methods and no knowledge of what comes before or after.

## Patterns

| Pattern | Where | Why |
|---|---|---|
| [Adapter](#adapter) | `TelemetrySource` implementations, `LLMClient` | Isolate external formats |
| [Strategy](#strategy) | Checks, fusion policy, planner, classifier | Vary an algorithm through configuration |
| [Observer](#observer) | Event bus subscriptions | Decouple producers from consumers |
| [Factory](#factory-and-plugin-registry) | Injectors, rules, detectors, skills | Build from configuration, with no code changes |
| [State](#state) | Diagnostic and stream state machines | Make transitions explicit and testable |
| [Decorator and Composite](#decorator-and-composite) | Combined faults, stage wrappers | Stack behaviour without modifying the wrapped class |

### Adapter

**What.** Converts an external interface into the one the system expects.

**Why.** FR1 and NFR13: replay, simulation and live robot must look identical to the pipeline. The dataset's quirks, such as `action` being hand-first, stay in one class.

**How.** `ReplayAdapter`, `SimAdapter` and `G1Adapter` implement `TelemetrySource`. The interface has no write operation, which is also how NFR17 is enforced.

### Strategy

**What.** A family of interchangeable algorithms behind one interface.

**Why.** Rules and ML must contribute side by side (FR17, FR18), the fusion policy must be configurable (FR21), and planners must be swappable (FR54).

**How.** `DiagnosticCheck`, `FusionPolicy`, `HypothesisRanker`, `DiagnosisPlanner`.

### Observer

**What.** Subscribers are notified of events without the publisher knowing them.

**Why.** Adding a consumer, such as the log or a future dashboard, must not touch any publisher.

**How.** `bus.subscribe(topic, handler, policy, bound)` in the composition root.

### Factory and plugin registry

**What.** Objects are created from a name in configuration.

**Why.** FR12, FR24, NFR10 and NFR11. It is the mechanism that makes "one class plus one configuration entry" true: the factory contains no list of known classes, only a way of loading them.

**How.** Config entries name a class by dotted path, `package.module:ClassName`, and are validated against the interface when loaded. See [Configuration](../design/configuration.md#plugin-loading).

### State

**What.** An object's behaviour depends on its state, and each state is explicit.

**Why.** Transition rules T1–T7 are the heart of goal G2 and must match the RASD one to one.

**How.** A transition table of `(state, guard, target, action)` with pure guard functions. A table is preferred to a class per state because each row maps directly to a row in RASD Table 3.1. This still gives the benefit of the pattern, and the Design Document should describe it as a table-driven State pattern.

### Decorator and Composite

**What.** Decorator wraps an object to add behaviour. Composite treats a group as one.

**Why.** FR14: simultaneous faults, possibly on the same target. FR13: runtime faults must affect a stage without changing it.

**How.** `FaultInjectingSource` decorates a source. `CompositeInjector` chains value injectors in order. `StallingStage` and `SlowStage` decorate a stage handler.

**Next:** [Technology and deployment](stack.md)
