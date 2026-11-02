# RASD review findings

This is a review of **RASD v0.1** against the real dataset and against itself. Every finding below can be checked. Data findings come from `tools/dataset_probe.py` and the dataset's documentation; consistency findings come from reading the document, and from `tools/check_traceability.py`.

The RASD is the team's document, so nothing here has been changed in it. These are proposals for v1.0.

## Summary

| # | Finding | Severity | Affects |
|---|---|---|---|
| A1 | No leg or waist commands in the data | **High** | S2, DA2, FR17, F9–F12 |
| A2 | Episodes are shorter than scenarios assume | **High** | S2, NFR6, timers |
| A3 | Tracking is much noisier than "bounded" suggests | **High** | DA2, tracking rule |
| A4 | Signals depend on the dataset format | Medium | SP1, adapter |
| A5 | Monotonic source clock is unverified | Medium | DA3 |
| A6 | Legs barely move | Medium | Fault evaluation |
| A7 | Dataset figures and licence | Low | §1.2, §2.6.2 |
| B1 | FR8 and FR28 can be read as contradictory | Medium | FR8, FR28, F5 |
| B2 | The state machine does not guarantee NFR7 | **High** | T1, NFR7 |
| B3 | Guided evidence could confirm a fault alone | Medium | FR53, DA8, S12 |
| B4 | Missing evidence could look like recovery | Medium | FR35, T2, T5 |
| B5 | Table 2.17 omits some mappings | Low | §2.6.4 |
| B6 | Injection point of F19 | Low | Table 2.2 |
| B7 | The ID scheme uses "D1" ambiguously | Low | Project plan |

## Data findings

### A1. No leg or waist commands

**Evidence.** The dataset's schema has `sol_q` (14 arm), `left_angles` and `right_angles` (7 per hand). Nothing covers the 15 leg and waist joints. The lite `action` has 28 values, all accounted for by arms and hands.

**Problem.** S2 has the "tracking-error rule" produce evidence for the **left knee**. This cannot happen. DA2 is true only for arms and hands. F9–F12 can't be observed on legs.

**Proposal.**

- Narrow DA2 and F9–F12 to joints with recorded commands.
- Rewrite S2 on an arm joint. The scenario reads the same with "left elbow" and "left arm".
- Optionally, add a scenario for a drift on a leg, showing the detection of a change on a nearly constant signal without a command.

### A2. Episodes are shorter than the scenarios assume

**Evidence.** G1 lite: 1,779,287 frames across 4,064 episodes at 30 Hz, or about 14.6 s per episode and 16.5 h in total.

**Problem.** S2's onset at 20 s is after the average episode has ended, and the following confirm, acknowledge, clear and return to healthy needs more time still. NFR6's 60 minutes at 5× requires 5 hours of data in one session.

**Proposal.** Set onset relative to the episode, for example 3 s, or use long episodes. Add an explicit requirement that the harness can chain episodes. The design already covers this under [chaining episodes](../design/ingestion.md#chaining-episodes). Add `EpisodeBoundary` to the shared phenomena.

### A3. Tracking is much noisier than "bounded" suggests

**Evidence.** In 40 episodes, the command-to-measure lag is 5–14 frames (167–467 ms), and the lag-compensated p95 residual is up to 0.345 rad. Per-joint p99 reaches 0.66 rad.

**Problem.** DA2's "bounded tracking error" holds, but only with a large bound. A fixed threshold would raise false alarms, and small F12 or F10 faults may not be separable from nominal teleoperated motion. It is also unclear whether the lag is physical, or an offset in the recording. See [data question D5](decisions.md#data-questions).

**Proposal.** State in DA2 that the bound is per joint and calibrated from data. Report F10 and F12 detection as a function of fault magnitude, rather than as a single number.

### A4. Signals depend on the dataset format

**Evidence.** `tau_ff` and original timestamps exist only in raw. The lite format has no IMU, odometry or tactile data ([format table](../overview/dataset.md#the-three-available-formats)).

**Proposal.** State in §2.6.2 which format is used. Raw for replay, lite for bulk training.

### A5. Monotonic source clock is unverified

**Evidence.** Raw `time` is documented as a UNIX timestamp. LeRobot timestamps are generated as frame index / 30.

**Problem.** DA3 assumes a monotonic robot clock. Wall clocks can step backwards. The system's ordering depends on it.

**Proposal.** Verify in W1 on raw data. If non-monotonic values appear, the adapter assigns monotonic time from frame order and the RASD documents this.

### A6. Legs barely move

**Evidence.** The median largest leg or waist joint range per episode is 0.028 rad, and only 3 of 40 sampled episodes exceed 0.2 rad.

**Problem.** Although the fault model treats all joints alike, its results for legs would say little about faults during motion.

**Proposal.** Report arm and leg results separately, and consider selecting loco-manipulation tasks to widen the coverage.

### A7. Dataset figures and licence

**Evidence.** The RASD quotes over 10,000 episodes across about 260 tasks, for both robots. The G1 subset is 4,064 episodes across 247 tasks. The dataset README says "MIT License" only, while the RASD says MIT and Apache 2.0.

**Proposal.** Quote the G1 figures in addition to the overall ones. Check the licence ([D7](decisions.md#data-questions)).

## Consistency findings

### B1. FR8 and FR28 can be read as contradictory

**Text.** FR8 treats "missing or non-numeric (NaN) values" as "evidence of a sensor fault". FR28 attributes "missing or delayed data to the communication layer or to the monitoring system" and forbids reporting it "as a fault of a joint or sensor". F5 (Missing/NaN) sits in the Sensor layer.

**Problem.** "Missing" appears in both, with opposite attribution.

**Proposal.** Distinguish them explicitly:

- A sample **arrives** with invalid values → sensor (FR8, F5).
- A sample **does not arrive** → communication or monitoring (FR28, F14, F16).

The [localizer](../design/classify-localize.md#faultlocalizer) already implements this.

### B2. The state machine does not guarantee NFR7

**Text.** NFR7 requires consecutive HEALTHY↔SUSPECTED transitions to be at least T<sub>dwell</sub> apart. T2 (SUSPECTED → HEALTHY) has a dwell guard, but T1 (HEALTHY → SUSPECTED) has none.

**Problem.** After T2 at time *t*, evidence jumping past θ<sub>enter</sub> at *t* + 33 ms fires T1 immediately, and breaks NFR7. Hysteresis alone doesn't prevent this: it stops small fluctuations, not a large swing. FR30 doesn't allow for a wait either.

**Proposal.** Add a guard to T1 and FR30: *and time since the last HEALTHY↔SUSPECTED transition ≥ T<sub>dwell</sub>*. First detections are unaffected. The alternative is to weaken NFR7 to "evidence fluctuating within the hysteresis band", which would be a real loss of guarantee. The [engine](../design/diagnostic-engine.md#addition-re-arm-guard-for-nfr7) assumes the guard.

### B3. Guided evidence could confirm a fault alone

**Text.** DA8 treats LLM answers as untrusted, FR53 lets them in as evidence, and S12 says "confirmation still follows the state machine".

**Problem.** Following the state machine isn't sufficient: a persistently confident LLM answer holding *e* ≥ θ<sub>conf</sub> for T<sub>conf</sub> would confirm a fault with no other support.

**Proposal.** Add a requirement that guided evidence alone cannot reach θ<sub>conf</sub>. The [fusion design](../design/fusion.md#guided-evidence-is-capped) caps it.

### B4. Missing evidence could look like recovery

**Text.** T2 and T5 fire on *e < θ<sub>exit</sub>*. FR28 says stale streams should give "missing data". But the RASD doesn't say what *e* is when no check can evaluate.

**Problem.** If absent evidence is read as zero, a stream dying during a joint fault would clear the fault: goal G3 turned upside down.

**Proposal.** Add a requirement that a component's state doesn't move toward healthy without evaluated evidence. The [engine](../design/diagnostic-engine.md#addition-missing-evidence) handles this through `coverage`.

### B5. Table 2.17 omits some mappings

**Evidence.** `tools/check_traceability.py` compares each requirement's Goals column with Table 2.17. These entries are in the requirement tables, but not in the mapping:

| Goal | Missing from Table 2.17 |
|---|---|
| G2 | FR29 |
| G3 | FR4, FR9, FR10 |
| G5 | NFR18 |
| G6 | FR38, FR44 |
| G7 | NFR16 |

**Proposal.** Add them. It's a small fix, but consistency is graded.

### B6. Injection point of F19

**Text.** Table 2.2 gives "Pipeline runtime" for clock skew, and FR13 follows suit.

**Problem.** Source clocks diverging is a property of the *robot's streams*, and the natural injection point is the source wrapper.

**Proposal.** Change the table's entry to "Stream". Layer stays as Monitoring system, if the team prefers.

### B7. The ID scheme uses "D1" ambiguously

**Text.** The plan's working rules give an example ID of "D1" for assumptions, while D1 also means Deliverable 1, and the RASD uses "DA".

**Proposal.** Use DA throughout.
