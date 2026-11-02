# Risks and cut order

!!! baseline "Baseline"
    The first five risks and the cut order are from the project plan. The rest come from this documentation's data check.

The main risk is losing weeks to holidays or exams. W13 is kept as buffer, and the secondary objective is the first thing to cut.

## Risks

| Risk | Effect | Mitigation |
|---|---|---|
| Holidays and exam sessions inside the 13 weeks | Fewer working days | Documents front-loaded; W13 kept free as buffer |
| Learning curve of the chosen stack | Implementation starts late | Technical spikes in W2–W4 |
| Dataset surprises (fields, joint order, size) | Fault model and rules need rework | Data checked in W1. Several surprises have [already been found](rasd-review.md). |
| Orchestrator LLM/VLM overruns (API cost, nondeterminism) | Time taken from core features | Secondary objective, last increment, deterministic planner as fallback |
| Documents drift from the code | Inconsistency, which is graded | v1.1 update of both documents in W12 |
| Large nominal residuals in teleoperated motion | Tracking rules generate false alarms, or catch only large faults | Lag compensation, per-joint calibration; report honestly per fault magnitude |
| ML adds little beyond rules | The hybrid looks no better than the baseline | Report as is: the project's value is the architecture and the honest comparison |
| M3 depends on Increment 4 | Critical milestone comes late | Build `ComponentFsm` first in Increment 4, or earlier |

## Cut order

If time runs short, cut in this order:

1. The orchestrator LLM/VLM (keep only the deterministic planner, or drop the feature).
2. Implementations of the simulation and live-robot adapters (keep their interface and the replay adapter).
3. Number of fault types implemented: see the [proposed tiers](../requirements/fault-catalogue.md#coverage-against-the-available-data).
4. UI polish.

**Never cut:** the event-driven core, the diagnostic state machine, rules + ML fusion, backpressure and the extensibility demo. These are the instructor's conditions for approval.
