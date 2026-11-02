# Scenarios

!!! baseline "Baseline"
    From RASD v0.1 §2.1. Thresholds such as θ<sub>enter</sub> are defined under [state machines](state-machines.md); fault IDs under [fault catalogue](fault-catalogue.md).

| | Scenario | Exercises | Goal |
|---|---|---|---|
| S1 | Monitoring a nominal episode | Normal operation, no false alarm | G1, G2 |
| S2 | Encoder drift on a single joint | The whole path, from evidence to clearing | G1, G5 |
| S3 | Stuck joint and ambiguous hypotheses | Honest ambiguity, localization | G1 |
| S4 | Degraded and interrupted telemetry link | Reordering, staleness, correct attribution | G3 |
| S5 | Pipeline overload at high replay rate | Backpressure, visible loss of coverage | G3 |
| S6 | Borderline evidence | Hysteresis and dwell | G2 |
| S7 | Disagreement between rules and ML | Evidence conflict | G2, G5 |
| S8 | Simultaneous faults | Fault composition | G1, G6 |
| S9 | Stalled pipeline component | Self-monitoring, partial operation | G3 |
| S10 | Adding a new fault type | Extensibility | G4 |
| S11 | Evaluation campaign | Metrics against baseline | G6 |
| S12 | Operator-guided diagnosis | Orchestrator and skills | G7 |

### S1 Monitoring a nominal episode

An operator opens the user interface, selects the dataset replay as telemetry source, chooses a G1 episode in which the robot picks up a cup, leaves the fault scenario empty and starts a session at nominal replay rate. The system receives the joint, IMU, odometry and hand-pressure streams at their own rates, aligns them in time and evaluates its checks on sliding windows. Small transient deviations produce low-score evidence that remains below θ<sub>enter</sub>, so every joint and body region stays HEALTHY. The health panel shows all queues well below their bounds and no stale stream. At the end of the episode the operator stops the session and its event log is saved.

### S2 Encoder drift on a single joint

A test engineer configures a scenario with an encoder drift (F2) on the left knee, starting 20 s after the beginning of the episode, and starts the replay; an operator watches the session. As the drift grows, the tracking-error rule and the ML detector produce evidence of increasing score for the left knee joint. When the fused evidence exceeds θ<sub>enter</sub>, the left knee becomes SUSPECTED and the left leg is highlighted. The evidence remains above θ<sub>conf</sub> for T<sub>conf</sub>, so the diagnosis becomes CONFIRMED and an alert reports "left knee: encoder drift" with its confidence, within 2 s of the last contributing sample. The operator opens the evidence trail, sees the contributing rule and detector results and the samples they came from, and acknowledges the alert; the state becomes ACKNOWLEDGED. When the injection ends, the evidence falls below θ<sub>exit</sub> for T<sub>clear</sub>, the joint becomes CLEARED, and later HEALTHY.

!!! warning "Not executable as written"
    The dataset has no leg commands and episodes average about 14.6 s. See [finding A1](../project/rasd-review.md#a1-no-leg-or-waist-commands) and [finding A2](../project/rasd-review.md#a2-episodes-are-shorter-than-the-scenarios-assume) for a proposed rewrite.

### S3 Stuck joint and ambiguous hypotheses

In a replayed episode the measured angle of the right elbow stops changing while its commanded target keeps moving (F9). The command/measurement inconsistency rule and the tracking-error rule both produce strong evidence. From telemetry alone, a stuck joint and a frozen encoder (F4) look alike, so the system reports both hypotheses with their confidences instead of choosing one arbitrarily. The diagnosis is localized to the right elbow and the right arm. The operator, who can see the robot, uses this information to decide what to inspect.

### S4 Degraded and interrupted telemetry link

A test engineer configures packet loss (F14) on the IMU stream and out-of-order delivery (F15) on the joint stream, followed by a three-second interruption (F16) of the IMU stream. Out-of-order joint samples that arrive within the lateness window W<sub>late</sub> are reordered and processed; samples arriving later are discarded and counted. The IMU stream is first reported as degraded and, during the interruption, as stale; a communication fault on the IMU stream is suspected and then confirmed. Checks that need IMU data report that data are missing instead of producing evidence against joints, so no joint fault is raised. When the stream resumes, its health recovers and the communication fault is cleared according to the state machine.

### S5 Pipeline overload at high replay rate

A test engineer replays an episode at 5× the nominal rate. The ML detector can no longer keep up with the incoming windows and its input queue reaches its configured bound. The system applies the declared backpressure policy (for example, dropping the oldest windows), so no queue exceeds its bound. The health panel shows the number of discarded windows, and a monitoring-system fault "pipeline overload" (F17) is confirmed so that the operator knows that diagnostic coverage is reduced. When the replay rate returns to 1×, the queue drains and the overload fault is cleared.

### S6 Borderline evidence

A scripted scenario makes the evidence for a wrist joint fluctuate around θ<sub>enter</sub>. The joint becomes SUSPECTED at the first crossing and remains SUSPECTED for at least the dwell time T<sub>dwell</sub>; it returns to HEALTHY only when the evidence falls below the lower threshold θ<sub>exit</sub>. Small fluctuations around θ<sub>enter</sub> therefore do not make the joint alternate between HEALTHY and SUSPECTED, and the operator is not distracted by flickering states.

### S7 Disagreement between rules and ML

A slight increase of noise on a hip encoder (F3) stays within the tolerance of every deterministic rule, while the ML detector reports an anomaly. The fusion policy does not silently resolve the disagreement: it records an evidence conflict for the hip joint, which the user interface marks with a dedicated indicator. The test engineer later reviews all conflicts of the session in the event log to tune thresholds and detectors.

### S8 Simultaneous faults

A test engineer combines an encoder drift (F2) on the left shoulder with packet loss (F14) on the joint stream. The system diagnoses both: a communication fault on the joint stream and a drift on the left shoulder joint. The drift is not explained away by the packet loss, and the evaluation reports detection and localization separately for each injected fault.

### S9 Stalled pipeline component

During a validation run, the test engineer injects a stall (F18) into the fault classifier, which stops publishing its heartbeat. After the configured heartbeat timeout, the system reports a monitoring-system fault "stalled component: classifier". The operator is warned that fault classification is unavailable; anomaly detection and the deterministic rules keep running and still produce evidence.

### S10 Adding a new fault type

A developer wants to support a new fault, a saturated hand-pressure sensor. They write one new injector class that implements the injector interface and add one entry to the configuration; they then write one new rule that detects saturation and register it through the configuration. After running the automated tests and a validation campaign, the new fault type appears in the evaluation report. The commit diff contains only new files and configuration entries: no existing component was modified.

### S11 Evaluation campaign

A test engineer selects a set of episodes and fault scenarios, single and combined, with fixed random seeds, and runs them twice in batch: once with all checks (hybrid mode) and once with deterministic rules only (rules-only baseline). For every implemented fault class the system produces the detection rate, false-alarm rate, detection delay and localization accuracy of both modes, together with the success rate of guided diagnosis on a set of scripted symptom reports, and exports them as a report.

### S12 Operator-guided diagnosis

While supervising the robot, an operator notices that the left arm seems to vibrate and types "the left arm is vibrating". The diagnosis orchestrator selects the relevant diagnostic skills (frequency analysis of the left-arm joints, tracking-error check of the left arm and a left/right symmetry comparison) and runs them. The results show an oscillation of the left elbow, so the orchestrator also looks at the most recent camera frames. It then ranks its hypotheses, with oscillation of the left elbow (F11) first. The ranked hypotheses, the skills that were run and their results are shown to the operator, and the conclusions enter the diagnostic process as evidence: the left elbow becomes SUSPECTED, while confirmation still follows the state machine. The orchestrator never raises an alert itself and never commands the robot.
