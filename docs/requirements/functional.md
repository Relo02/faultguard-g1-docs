# Functional requirements

!!! baseline "Baseline"
    From RASD v0.1 §2.4. Unless stated otherwise, "the system" is the Diagnostic System. *Open* marks a `[TODO]` from the RASD, tracked in [Open decisions](../project/decisions.md).

## Telemetry acquisition

| ID | Requirement | Goals |
|---|---|---|
| FR1 | The system shall acquire telemetry through a single source interface, regardless of whether the source is a dataset replay, a simulation or a live robot. | G3, G4 |
| FR2 | The system shall ingest each telemetry stream independently, at the stream's own rate. | G3 |
| FR3 | The system shall record, for every sample, its source timestamp and its receive timestamp. | G3, G5 |
| FR4 | The system shall align streams with different rates on a common time base before evaluating checks that combine more than one stream. | G1, G3 |
| FR5 | The system shall accept samples that arrive late or out of order within a configurable lateness window W<sub>late</sub>, and shall process them in source-timestamp order. | G3 |
| FR6 | The system shall discard samples that arrive later than W<sub>late</sub>, count them per stream, and report the count as part of the monitoring-system health. | G3 |
| FR7 | The system shall detect when a stream has no samples for at least a configurable time T<sub>stale</sub>, and shall mark the affected data as missing instead of silently filling the gap. | G3, G1 |
| FR8 | The system shall accept samples with missing or non-numeric (NaN) values without interrupting processing, and shall treat such values as evidence of a sensor fault. | G3, G1 |
| FR9 | The Validation Harness shall replay dataset episodes at a configurable replay rate from 1× to at least 5×. | G6, G3 |
| FR10 | The Validation Harness shall split recorded frames into independent per-sensor streams with configurable rates and timing jitter. | G3, G6 |

## Fault injection (Validation Harness)

| ID | Requirement | Goals |
|---|---|---|
| FR11 | The Validation Harness shall let the test engineer define a fault scenario in configuration, specifying for each fault its type, target, onset, duration and parameters. | G6 |
| FR12 | The Validation Harness shall create the fault injectors of a scenario from its configuration, without code changes. | G6, G4 |
| FR13 | The Validation Harness shall support injection on sample values, on streams (timing, loss, order, interruption) and on the runtime of the monitoring pipeline (load, stalls, clock skew). | G6 |
| FR14 | The Validation Harness shall support scenarios with several simultaneous faults, including faults on the same target. | G6 |
| FR15 | The Validation Harness shall record the ground truth of every injected fault, and the ground truth shall not be accessible to the checks and to the diagnostic state machine. | G6 |
| FR16 | Fault injection that involves randomness shall be reproducible from a configured seed. | G6 |

## Evidence production

| ID | Requirement | Goals |
|---|---|---|
| FR17 | The system shall evaluate deterministic rules including at least: excessive tracking error; stale telemetry; physically impossible values (outside joint limits or physical ranges); missing data; inconsistency between commands and measurements. | G1 |
| FR18 | The system shall evaluate machine-learning anomaly detectors on windows of telemetry. | G1 |
| FR19 | Every check shall publish its result as evidence that states the monitored component, the check, a score, the time window, optionally a suspected fault type, and a correlation ID identifying the samples used. | G1, G5 |
| FR20 | No individual check result shall raise an alert; alerts shall be raised only on confirmation by the diagnostic state machine (FR31). | G2 |
| FR21 | The system shall combine the evidence of different checks on the same component according to a configurable fusion policy. | G1, G2 |
| FR22 | When rule-based and ML-based evidence on the same component and time window disagree by more than a configurable margin, the system shall record an evidence conflict and show it to the operator, without discarding either. | G2, G5 |
| FR23 | The system shall allow ML detectors to be disabled for a session, so that it runs as the rules-only baseline. | G6 |
| FR24 | The system shall allow each check to be enabled, disabled and parametrized through configuration. | G4 |

## Fault classification and localization

| ID | Requirement | Goals |
|---|---|---|
| FR25 | For every component with anomalous evidence, the system shall produce a list of fault hypotheses from the fault catalogue, ranked by confidence. | G1 |
| FR26 | When the available telemetry does not discriminate between fault types, the system shall report every hypothesis whose confidence exceeds a configurable threshold, not only the most likely one. | G1, G2 |
| FR27 | The system shall localize every diagnosis to a joint, sensor, telemetry stream or pipeline component, and to the body region that contains it, where applicable. | G1 |
| FR28 | The system shall attribute missing or delayed data to the communication layer or to the monitoring system, and shall not report it as a fault of a joint or sensor. | G1, G2 |

## Diagnostic state management

The thresholds satisfy θ<sub>exit</sub> < θ<sub>enter</sub> ≤ θ<sub>conf</sub>. See [state machines](state-machines.md).

| ID | Requirement | Goals |
|---|---|---|
| FR29 | The system shall maintain, for every monitored component, a diagnostic state among HEALTHY, SUSPECTED, CONFIRMED, ACKNOWLEDGED and CLEARED. | G1, G2 |
| FR30 | The system shall move a HEALTHY component to SUSPECTED when its fused evidence reaches θ<sub>enter</sub>. | G1 |
| FR31 | The system shall move a SUSPECTED component to CONFIRMED when its fused evidence stays at or above θ<sub>conf</sub> for at least T<sub>conf</sub>, and shall then publish a diagnostic confirmation (`DiagnosticConfirmed`). | G1, G2 |
| FR32 | The system shall return a SUSPECTED component to HEALTHY only when its fused evidence is below θ<sub>exit</sub> and it has been SUSPECTED for at least T<sub>dwell</sub>. | G2 |
| FR33 | A CONFIRMED component shall remain CONFIRMED until the operator acknowledges it, even if its evidence disappears. *Open: confirm this latching policy.* | G1, G2 |
| FR34 | The system shall move a component from CONFIRMED to ACKNOWLEDGED only upon an operator acknowledgement. | G1 |
| FR35 | The system shall move an ACKNOWLEDGED component to CLEARED when its fused evidence stays below θ<sub>exit</sub> for at least T<sub>clear</sub>; a CLEARED component shall become HEALTHY after T<sub>dwell</sub>, or SUSPECTED again if its evidence reaches θ<sub>enter</sub>. | G2 |
| FR36 | Thresholds and times of the state machine shall be configurable per class of monitored component. | G2, G4 |
| FR37 | The system shall derive the state of a body region as the most severe state among its joints and sensors. *Open: agree on the severity order of states.* | G1 |

## Alerting and operator interaction

| ID | Requirement | Goals |
|---|---|---|
| FR38 | The system shall let the operator select the telemetry source, the episode, the fault scenario and the replay rate, and start, pause and stop a monitoring session. | G1, G6 |
| FR39 | Upon confirmation of a diagnosis, the system shall raise an alert stating the component, its body region, the ranked fault hypotheses with their confidence, and the time of confirmation. | G1 |
| FR40 | During a session, the system shall display the current diagnostic state of every monitored component, grouped by body region. | G1 |
| FR41 | The system shall let the operator acknowledge an alert, and shall record the time of the acknowledgement. | G1 |
| FR42 | The system shall let the operator inspect, for any diagnosis, the evidence that supports it, any related evidence conflict, and the telemetry samples from which the evidence was computed. | G5 |
| FR43 | The system shall display the health of the monitoring system: queue occupancy, discarded or coalesced data, stale streams and stalled components. | G3 |
| FR44 | The system shall record the evidence, state transitions, alerts and acknowledgements of a session in a persistent event log that can be reviewed after the session. | G5, G6 |

## Self-monitoring

| ID | Requirement | Goals |
|---|---|---|
| FR45 | The system shall monitor the liveness of each of its pipeline components and, when a component misses its heartbeat for a configurable timeout, shall produce evidence of a stalled component (F18). | G3 |
| FR46 | Every internal queue of the system shall have a configured bound; when a queue is full, the system shall apply the declared backpressure policy (dropping the oldest items or coalescing them). | G3 |
| FR47 | The system shall report data discarded or coalesced by the backpressure policy as evidence of pipeline overload (F17), stating the amount of affected data. | G3 |
| FR48 | The system shall detect when the source clocks of different streams diverge beyond a configurable tolerance, and shall report it as a clock-skew fault (F19). | G3 |

## Operator-guided diagnosis (secondary objective)

| ID | Requirement | Goals |
|---|---|---|
| FR49 | The system shall let the operator submit a symptom description in natural language during a session. | G7 |
| FR50 | The orchestrator shall select from the skill registry the skills relevant to the symptom, run them, reason on their results, and iterate until it can rank fault hypotheses or a configurable maximum number of iterations is reached. | G7 |
| FR51 | The skill registry shall provide at least: a tracking-error check per joint group; frequency analysis for oscillation; a telemetry-staleness check; a left/right symmetry comparison; and retrieval of recent camera frames. | G7 |
| FR52 | Diagnostic skills shall be read-only: they shall not change the diagnostic state of any component and shall not send anything to the robot. | G7, G2 |
| FR53 | The conclusions of the orchestrator shall enter the diagnostic process only as evidence; the orchestrator shall not raise alerts or change diagnostic states directly. | G7, G2 |
| FR54 | The system shall provide a deterministic, rule-based planner that can replace the LLM/VLM planner, selectable through configuration. | G7, G6 |
| FR55 | The system shall display the ranked hypotheses of a guided diagnosis together with the skills executed, their results and the justification given by the planner. | G7, G5 |
| FR56 | When the LLM/VLM service is unavailable or does not answer within a configurable timeout, the system shall inform the operator and *(Open: fall back to the rule-based planner, or abort?)*. | G7, G3 |

## Evaluation (Validation Harness)

The evaluation function is the only function that reads the ground truth of injected faults. Exact metric definitions are proposed under [Evaluation metrics](../verification/evaluation.md).

| ID | Requirement | Goals |
|---|---|---|
| FR57 | For every implemented fault class, in single-fault and in combined-fault scenarios, the Validation Harness shall compute detection rate, false-alarm rate, detection delay and localization accuracy. | G6 |
| FR58 | The Validation Harness shall run the same scenarios in rules-only mode and report its metrics side by side with those of the hybrid mode. | G6 |
| FR59 | For a set of scripted symptom reports, the Validation Harness shall compute the rate at which the injected fault is among the top-k hypotheses of the guided diagnosis, with k configurable. | G6, G7 |
| FR60 | The Validation Harness shall run a campaign of episodes and scenarios in batch, without operator interaction, and export its results in a machine-readable format together with a human-readable summary. | G6 |
