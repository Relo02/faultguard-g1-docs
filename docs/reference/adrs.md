# Decision records

!!! proposed "All records below have status *Proposed*"
    They are written so that the team can accept, change or reject each one. An accepted record should move to the Design Document.

## ADR-001: Python asyncio instead of ROS 2

**Context.** The plan leaves the stack open between Python asyncio with an internal bus and ROS 2. The main path is dataset replay on a laptop. Requirements include declared overload policies per queue (FR46), deterministic repeat runs (NFR15) and a bounded memory footprint.

**Decision.** Python ≥ 3.11 with `asyncio` and an in-process typed bus.

**Why.**

| Criterion | asyncio | ROS 2 |
|---|---|---|
| Per-queue overload policy, including coalesce-by-key | Built exactly as required | QoS offers keep-last; custom coalescing must be added on top |
| Deterministic replay with a virtual clock | Simple: single loop, run until quiescent | Harder: multiple nodes and DDS; `/clock` doesn't remove scheduling nondeterminism |
| Evaluation campaigns faster than real time | Natural | Awkward |
| Setup on team machines, CI | `pip install` | Larger, OS-dependent install |
| Live G1 integration | Needs an adapter | The G1's ecosystem has an advantage |
| "Real" distribution across processes | Not provided | Built in |

**Consequences.** The architecture's focus (events, bounded queues, patterns) is expressed in code the team writes and can explain, which suits a software engineering course. A single loop means CPU-heavy work must leave it. ROS 2 stays reachable: `G1Adapter` can bridge ROS 2 or DDS topics into `TelemetrySource`, without affecting the pipeline.

**Validation.** The event-bus spike must show that the loop holds at 5×. **If it doesn't, revisit this decision.**

## ADR-002: The engine takes state input directly from fusion

**Context.** The proposal lists the stages as a chain ending in `DiagnosticEngine`.

**Decision.** The engine consumes `EvidenceFused` directly and hypotheses from `FaultLocalized` asynchronously. See [why](../architecture/components.md#why-the-engine-does-not-sit-at-the-end-of-a-single-chain).

**Consequences.** S9 works, and exit transitions get low scores. An alert can appear before its hypotheses are final, so `AlertUpdated` is needed.

## ADR-003: Separate run modes for timing and reproducibility

**Context.** NFR15 requires reproducibility; NFR1–NFR3 need real timing; real-time drops depend on the machine.

**Decision.** `deterministic` and `realtime` modes. See [Two run modes](../architecture/concurrency.md#two-run-modes).

**Consequences.** Campaigns run fast and repeatably, and timing is tested separately. Deterministic metrics assume no overload, so a mention in the report is needed that overload's effect on quality isn't measured by the campaign. Stage code must not depend on which mode is running.

## ADR-004: Harness as a separate package

**Context.** FR15 requires ground truth to be inaccessible to the checks and the state machine.

**Decision.** `faultguard_harness` depends on `faultguard`, never the reverse, enforced by CI. The harness wraps sources and stages from outside.

**Consequences.** The separation is mechanically verifiable. FR38's scenario selection in the UI needs [a small factory interface](../design/ui.md#gateway-api).

## ADR-005: Table-driven state machine

**Context.** The proposal names the State pattern. RASD Table 3.1 lists transitions.

**Decision.** A transition table with pure guards, rather than one class per state.

**Consequences.** One-to-one mapping to the RASD, and exhaustive tests. The Design Document should state clearly that this is a table-driven realization of the pattern, so that the instructor can see the correspondence.

## ADR-006: Dotted-path plugins rather than a registry decorator

**Context.** NFR10–NFR13 forbid changing existing components when extending.

**Decision.** Configuration names classes by `module:Class`. See [Plugin loading](../design/configuration.md#plugin-loading).

**Consequences.** New code is never imported by existing code. A typo fails at start-up with a clear error. The configuration file holds code paths, so only trusted configuration may be loaded; this is acceptable for a research prototype.

## ADR-007: Noisy-OR fusion by default

**Context.** FR21 requires a configurable policy.

**Decision.** Noisy-OR, with weights, with `MaxFusion` as a comparison baseline.

**Consequences.** One strong witness is enough, and weak ones accumulate. Correlated checks are overstated, which the weights offset. Weights are tuning parameters, and they must be set on validation data only.

## ADR-008: Report arms and legs separately

**Context.** The [measurements](../overview/dataset.md) show that the legs barely move and have no commands.

**Decision.** All evaluation results are split by arm, hand and leg.

**Consequences.** Aggregate numbers can't hide weak leg coverage.
