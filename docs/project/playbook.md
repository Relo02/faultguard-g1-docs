# Step-by-step playbook

This is the [project plan](roadmap.md) expanded into steps: for each one, what to read on this site, what to produce, and how to know it is done. Tasks are from the plan. *Read first* links and *done when* criteria are proposed here.

Owners are not assigned yet; see [Open decisions](decisions.md).

## Phase 0: Setup (W1)

**Goal.** Everyone can work, and the risky data questions are answered.

**Read first:** [Deliverables](../overview/deliverables.md), [Telemetry data](../overview/dataset.md), [Technology](../architecture/stack.md), [ADR-001](../reference/adrs.md#adr-001-python-asyncio-instead-of-ros-2).

- [ ] Prepare the private repo, invite `matteocamilli`, and add a directory per deliverable. The team's private repo already exists under a different name from the one in the plan; decide which stands.
- [ ] Set up the LaTeX project, with shared preamble, front page and table of contents.
- [ ] Decide the tech stack.
- [ ] Agree roles and a weekly meeting.
- [ ] Download one or two G1 tasks in **raw** format. Run `tools/dataset_probe.py`, then extend it to what it doesn't yet cover:
    - [ ] Is raw `time` monotonic? How much jitter is there? (DA3)
    - [ ] What are the IMU units, and do they match odometry? (F6, F7)
    - [ ] Reading ranges of `usable_readings` (F8)
    - [ ] Is `sol_q` what the controller received? Compare to the `armtime` / `iktime` timing (DA2)
    - [ ] Which `tau_ff` values appear?
    - [ ] Does the licence on each format match what the RASD cites?

**Done when:** M0 is closed, and the [data questions](decisions.md#data-questions) have answers written down.

## Phase 1: RASD (W1–W4)

**Goal.** A v1.0 RASD that matches reality and has no open TODOs.

**Read first:** [RASD review findings](rasd-review.md), [Open decisions](decisions.md).

v0.1 already covers most of this phase, so the work is mainly review:

- [ ] Goals, world/machine boundary and shared phenomena (W1–W2): check against the data.
- [ ] Scenarios and domain model (W2): rewrite S2, and fix scenario timings.
- [ ] Functional and non-functional requirements, assumptions, dependencies, constraints (W2–W3): resolve every `[TODO]`, and fix [the findings](rasd-review.md).
- [ ] Diagnostic state machine and sequence diagrams (W3): add the T1 guard if approved.
- [ ] Mark mandatory faults, using the [proposed tiers](../requirements/fault-catalogue.md#coverage-against-the-available-data).
- [ ] Review against the guideline; push v1.0 (W4).

**Done when:** M1 is closed; no `[TODO]` remains; all three members have reviewed it.

## Technical spikes (W2–W4, parallel)

**Goal.** Test the risky design ideas before writing them into the Design Document. Spikes are throwaway code that answers a question.

| Spike | Read first | Question to answer | Done when |
|---|---|---|---|
| Replay adapter | [Ingestion](../design/ingestion.md) | Can a recorded G1 episode stream at 30 Hz, split into independent streams, with stable pacing? | A script shows per-stream rates at 1× and 5× |
| Event bus with bounded queue | [Event bus](../design/event-bus.md), [Concurrency](../architecture/concurrency.md) | Does one asyncio loop hold 5× load? How much latency does it add? What happens with a deliberately slow consumer? | A benchmark gives numbers for the [budget](../architecture/runtime.md#latency-budget-for-nfr1), and asyncio vs ROS 2 is confirmed |

## Phase 2: Design Document (W4–W7)

**Goal.** Turn this site's proposals into an agreed, reviewed Design Document.

**Read first:** [the mapping from chapters to pages](../overview/deliverables.md#d2-design-document-structure).

| Task | Week | Input |
|---|---|---|
| Component view and interfaces | W4–W5 | [Components](../architecture/components.md), [Events](../architecture/events.md) |
| Class view diagrams | W5–W6 | [Low-level design](../design/index.md) |
| Runtime sequence diagrams; concurrency and backpressure | W6 | [Runtime](../architecture/runtime.md), [Concurrency](../architecture/concurrency.md) |
| Styles and patterns; UI mockups | W6 | [Patterns](../architecture/patterns.md), [UI](../design/ui.md) |
| Traceability tables; implementation, integration and test plan | W7 | [Traceability](../verification/traceability.md), [Test strategy](../verification/strategy.md) |
| Review; push v1.0 | W7 | Update the site where the team decided differently |

**Done when:** M2 is closed, all IDs resolve, and all [decision records](../reference/adrs.md) are accepted or replaced.

## Phase 3: Implementation (W5–W11)

**Rule:** the pipeline runs end-to-end at all times, with stubs for what doesn't exist yet.

### Increment 1 (W5–W6): the kernel and telemetry path

**Build:** [domain events](../design/domain-types.md), [event bus](../design/event-bus.md), [replay adapter, alignment and windowing](../design/ingestion.md), [logging](../design/alerts-log.md), CI running unit tests.

**Done when:** a command replays an episode and writes a log containing `WindowReady` events with sample references. Import contracts and property tests pass in CI.

### Increment 2 (W7–W8): faults and rules

**Build:** [fault injection framework](../design/fault-injection.md) (value and stream injectors, composition), [rule engine](../design/rules.md), calibration tool.

**Done when:** a scenario file injects F2 and F14 together, with a truth file produced, and rules give clearly higher evidence during the fault. False-alarm evidence on nominal held-out episodes is quantified.

### Increment 3 (W8–W9): evidence becomes hypotheses

**Build:** [ML detectors](../design/ml.md), [classifier and localizer](../design/classify-localize.md), [evidence fusion](../design/fusion.md).

**Done when:** `FaultLocalized` names the right joint for F2 and F12 on an arm, in rules-only and hybrid modes.

### Increment 4 (W9–W10): decisions, then overload

**Build first (needed for M3):** [`ComponentFsm` and `DiagnosticEngine`](../design/diagnostic-engine.md), minimal [`AlertManager`](../design/alerts-log.md).

**Build next:** [overload handling and health monitor](../design/self-monitoring.md).

**M3 done when:** replayed data with an injected fault reaches CONFIRMED and raises an alert, with automated tests passing.

**Increment done when:** S4, S5, S6 and S9 scenario tests pass.

### Increment 5 (W10–W11): the operator's view

**Build:** [operator UI](../design/ui.md), [deterministic planner, skills](../design/guided.md), then the LLM/VLM planner if time allows.

**M4 done when:** planned faults, rules + ML fusion, backpressure and operator UI all work.

## Phase 4: Verification (W9–W12)

**Read first:** [Test strategy](../verification/strategy.md), [Evaluation metrics](../verification/evaluation.md).

- [ ] Integration tests for each increment.
- [ ] System tests on replay scenarios, one per RASD scenario.
- [ ] Overload test at up to 5×; anti-oscillation test of the state machine.
- [ ] Extensibility demo: [add one new fault type and show the diff](../design/configuration.md#worked-example-adding-a-new-fault-s10).
- [ ] Evaluation report: detection rate, false alarms and detection delay against the rules-only baseline.

**Done when:** every requirement in [Traceability](../verification/traceability.md) has passing evidence or a recorded reason why not.

## Phase 5: Finalization (W12–W13)

- [ ] Update RASD and Design Document to v1.1, with revision history.
- [ ] README and installation instructions, tested on a clean machine by a member who didn't write them.
- [ ] Presentation and demo; rehearse the timing, as the fit to allowed time is graded.
- [ ] Final push to `main`.

**Done when:** M6 is closed, before the deadline. W13 is buffer, so nothing new should be planned for it.
