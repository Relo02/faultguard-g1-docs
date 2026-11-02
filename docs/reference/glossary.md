# Glossary

!!! baseline "Baseline"
    From RASD v0.1 §1.3. Fault, error and failure follow the dependability taxonomy of Avižienis et al.

## Definitions

| Term | Definition |
|---|---|
| Fault | The adjudged cause of an error, e.g. a drifting encoder or a lossy link. |
| Failure | A deviation of a component's delivered service from correct service. |
| Fault type | A class of faults in the [fault catalogue](../requirements/fault-catalogue.md). |
| Fault injection | The controlled alteration of telemetry, or of the monitoring pipeline, that emulates a fault and records its ground truth. |
| Fault scenario | A configured set of one or more injected faults applied to an episode. |
| Ground truth | The type, target and time interval of an injected fault. |
| Episode | One recorded run of a task in the dataset. |
| Replay rate | Ratio between replay speed and recording speed; 1× is nominal. |
| Monitored component | An element whose diagnostic state is tracked: a joint, a sensor, a body region, a telemetry stream or a component of the monitoring pipeline. |
| Body region | A group of joints: left/right arm, left/right leg, waist, left/right hand. |
| Diagnostic check | A deterministic rule, an ML detector or a diagnostic skill that produces evidence. |
| Evidence | A time-stamped statement, produced by a diagnostic check, that a monitored component behaves anomalously, with a score and optionally a suspected fault type. |
| Evidence conflict | Disagreement between rule-based and ML-based evidence on the same component and time window. |
| Diagnosis | The diagnostic state of a monitored component together with its ranked fault hypotheses and supporting evidence. |
| Alert | Notification to the operator that a diagnosis has been confirmed. |
| Hysteresis | Use of an exit threshold lower than the enter threshold, so that a state change is not reverted by small fluctuations of the evidence. |
| Dwell time | Minimum time spent in a diagnostic state before leaving it. |
| Lateness window | Maximum delay with which an out-of-order sample is still accepted. |
| Backpressure policy | The declared behaviour when data arrive faster than they can be processed, e.g. dropping the oldest windows or coalescing them. |
| Correlation ID | Identifier that links an alert to the evidence and samples behind it. |
| Rules-only baseline | Configuration in which only deterministic rules produce evidence. |
| Diagnostic skill | A read-only diagnostic test that the orchestrator can run. |
| Detection delay | Time between the onset of an injected fault and its confirmation. |

## Added by the design

| Term | Definition |
|---|---|
| Watermark | The source time up to which a stream, or all streams together, is considered complete. |
| Coalescing | Keeping only the newest queued item for a given key. |
| Coverage | Whether any required check could be evaluated on a component in the current period. |
| Hop | The time between consecutive sliding windows. |
| Residual | The difference between a joint's command and its measurement. |
| Composition root | The one place where all concrete components are created and connected. |

## Acronyms

| Acronym | Meaning |
|---|---|
| ADR | Architecture Decision Record |
| DA | Domain Assumption |
| DD | Design Document |
| FR | Functional Requirement |
| FSM | Finite State Machine |
| G | Goal |
| IMU | Inertial Measurement Unit |
| LiDAR | Light Detection and Ranging |
| LLM | Large Language Model |
| ML | Machine Learning |
| NaN | Not a Number |
| NFR | Non-Functional Requirement |
| RASD | Requirements Analysis and Specification Document |
| RGB-D | Colour image plus depth |
| SP | Shared Phenomenon |
| TTL | Time To Live |
| UI | User Interface |
| UML | Unified Modeling Language |
| VLM | Vision-Language Model |
