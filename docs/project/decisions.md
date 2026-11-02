# Open decisions

!!! proposed "Proposed"
    This page collects every open item from the RASD and the project plan, with a recommendation for each. **All of them are the team's to decide**, and none should be assumed settled. The design pages assume the recommended option where one is needed.

## Project organization

| # | Decision | Recommendation | Why |
|---|---|---|---|
| P1 | Official start date | Ask the instructor | Turns W1–W13 into dates |
| P2 | Owner of each phase and increment | Team | Not assigned yet |
| P3 | Tech stack | Python asyncio | [ADR-001](../reference/adrs.md#adr-001-python-asyncio-instead-of-ros-2) |
| P4 | Day of the weekly sync | Team | |
| P5 | LaTeX on Overleaf or local | Local from the repo; Overleaf can sync through Git if someone prefers it | One source of truth |
| P6 | Which private repo is official | Keep the one that already exists | It exists, with all three members |
| P7 | Student IDs on front pages and in file names | Leave out unless asked | The guideline does not require them |
| P8 | Is a public companion site acceptable? | Ask the instructor | The guideline asks for a private repo |

## RASD `[TODO]` items

| # | Where | Question | Recommendation |
|---|---|---|---|
| R1 | §2.1 | Trim or merge scenarios? Keep at least one per goal | Keep all 12. Each already has an automated test assigned, and the instructor can ask for fewer. |
| R2 | §2.4.2 | Which faults are mandatory? | The [Core tier](../requirements/fault-catalogue.md#coverage-against-the-available-data) |
| R3 | FR33 | Latching policy: stay CONFIRMED until acknowledged? | Yes. A fault that came and went is exactly what the operator should know about. |
| R4 | FR37 | Severity order of states | CONFIRMED > ACKNOWLEDGED > SUSPECTED > CLEARED > HEALTHY |
| R5 | FR56 | LLM unavailable: fall back or abort? | Inform the operator and fall back to the rule-based planner |
| R6 | §2.4.9 | Metric definitions | [Evaluation metrics](../verification/evaluation.md) |
| R7 | NFR2 | UI latency value | Keep 1 s |
| R8 | NFR6 | Long-run duration | 60 min at 5×; needs 5 h of chained episodes. 30 min is a fallback if run time is a problem. |
| R9 | NFR8 | Target values | [Tentative targets](../verification/evaluation.md#tentative-targets), fixed after the first campaign |
| R10 | NFR9 | k and target | k = 3, target 0.7 |
| R11 | NFR15 | Must order and timing also match? | In `deterministic` mode, yes: require the identical event sequence. A stronger property is easier to test. In `realtime`, no. |
| R12 | NFR18 | Interaction count | Keep two; the design needs one |
| R13 | NFR20 | Machine specification | The weakest team laptop. Record OS, CPU, RAM. |
| R14 | §3.2.1 | Must an ACKNOWLEDGED fault whose evidence grows again raise a new alert? | No new alert, but mark the existing diagnosis "worsening" in the UI once evidence passes θ<sub>conf</sub> again. A new alert for the same acknowledged fault risks alert fatigue. |
| R15 | DA1 | Screening episodes | Exclude episodes with extreme lag or residual from training, using the probe; record what's excluded |
| R16 | Ref. 3 | Access date | Add when finalizing |

## Decisions raised by the review

These come from the [RASD review findings](rasd-review.md).

| # | Decision | Recommendation |
|---|---|---|
| N1 | How to rewrite S2 | Use an arm joint, and a shorter onset |
| N2 | Add a re-arm guard to T1? | Yes |
| N3 | Cap guided evidence below θ<sub>conf</sub>? | Yes |
| N4 | Format of telemetry for replay | Raw for replay, lite for bulk training |
| N5 | LLM/VLM provider and model | Decide in W9–W10, if the feature is still in scope; the `LlmClient` port leaves this open |

## Data questions

To answer in W1 with `tools/dataset_probe.py` on raw data.

| # | Question | Affects |
|---|---|---|
| D1 | Is raw `time` monotonic, and how much jitter does it have? | DA3, FR10 |
| D2 | Is `sol_q` what the controller receives? What do `armtime` and `iktime` mean? | DA2, tracking rules |
| D3 | What are the IMU units and noise levels? Do IMU and odometry orientations agree? | F6, F7 |
| D4 | What are the ranges of `usable_readings`? | F8 |
| D5 | Is the 8-frame median lag a controller effect, a teleoperation artifact or a recording offset? | F10 |
| D6 | What is the distribution of episode lengths? | Scenario timing |
| D7 | Which licence applies? The README says MIT, the RASD says MIT/Apache-2.0 | RASD references |
