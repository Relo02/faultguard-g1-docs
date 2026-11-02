# Telemetry data

The whole system develops against one dataset, so its real contents limit what can be diagnosed. This page separates what the dataset's publishers state from what was measured here.

!!! success "Measured, not assumed"
    The figures below were produced by [`tools/dataset_probe.py`](https://github.com/Relo02/faultguard-g1-docs/blob/main/tools/dataset_probe.py) on 2 November 2026: 40 random G1 episodes from 28 tasks (seed 7, 9.6 minutes of data). They cover joints and commands from the *lite* format only. **IMU, odometry and hand-pressure signals were not inspected**; that remains part of task M0 in week 1.

## Source

[Humanoid Everyday](https://github.com/physical-superintelligence-lab/Humanoid-Everyday) (University of Southern California, 2025): teleoperated episodes on real Unitree G1 and H1 robots, recorded at 30 Hz. Only the G1 recordings are used, and because they are nominal behaviour, every fault label comes from controlled injection.

## The three available formats

They are not interchangeable. **Choosing the wrong one silently removes signals the fault catalogue needs.**

| Signal | Raw (`data.json` + files) | LeRobot full | LeRobot lite G1 |
|---|---|---|---|
| Arm, leg, hand joint angles | yes | yes | yes |
| Arm and hand commands | yes (`sol_q`, `left_angles`, `right_angles`) | yes (`action`) | yes (`action`) |
| Feed-forward torques `tau_ff` (arms only) | yes | **no** | **no** |
| IMU, odometry | yes | yes | **no** |
| Hand pressure | yes | yes (`observation.tactile.*`) | **no** |
| RGB / depth / LiDAR | yes | yes | RGB video only |
| Original wall-clock timestamp `time` | yes | **no**, frame index / 30 | **no**, frame index / 30 |
| Robots included | per task | G1 and H1 mixed | G1 only |
| Size | about 500 GB | about 1 TB | small: each episode's table is 70–170 KB, excluding video |

!!! proposed "Proposed: which format for what"
    - **Raw, one or two tasks at first**: for `ReplayAdapter`, because only this format has every signal and the real timestamps.
    - **Lite**: for training and calibrating arm and leg detectors over many tasks, and for early spikes.

    The first adapter should read the raw format through the publishers' `humanoid_everyday.Dataloader`.

## G1 signals per frame

| Field | Shape | Content |
|---|---|---|
| `time` | scalar | UNIX timestamp in seconds |
| `states.arm_state` | 14 | 0–6 left shoulder pitch, roll, yaw, elbow, wrist roll, pitch, yaw; 7–13 the same on the right |
| `states.leg_state` | 15 | 0–5 left hip pitch, hip roll, hip yaw, knee, ankle, ankle roll; 6–11 the same on the right; 12–14 waist yaw, roll, pitch |
| `states.hand_state` | 14 | Dex3 hands: 0–6 left thumb rotation, thumb lower/upper, middle lower/upper, index lower/upper; 7–13 the same on the right |
| `states.hand_pressure_state` | 9 per hand | Each with `sensor_id`, `sensor_type` ("A" or "B"), `usable_readings` (3) |
| `states.imu` | | `quaternion` (4, w-first), `accelerometer` (3), `gyroscope` (3), `rpy` (3) |
| `states.odometry` | | `position` (3), `velocity` (3), `rpy` (3), `quat` (4, w-first) |
| `actions.sol_q` | 14 | Arm joint solution from inverse kinematics: **the arm command** |
| `actions.tau_ff` | 14 | Arm feed-forward torques |
| `actions.left_angles`, `right_angles` | 7 each | **The hand commands** |
| `actions.armtime`, `iktime` | scalar | Timestamps |
| `actions.left_pose`, `right_pose`, `head_rmat` | 4×4, 4×4, 3×3 | Teleoperator targets |
| `image`, `depth`, `lidar` | 480×640×3, 480×640, about 6000×3 | Egocentric perception |

## What was measured, and why it matters

### There are no leg or waist commands

`actions` covers arms and hands only. In the sampled lite data, `action` has 28 values: **the first 14 are hands and the last 14 are arms**. The mean difference from the measured arm angles is 0.063 rad for the last 14, and 0.632 rad for the first 14. The publishers' README example concatenates them the other way round, so a wrong assumption here would silently corrupt every tracking check.

**Consequence.** Every check that compares a command to a measurement is impossible on 15 of the 43 joints. Joint and actuator faults F9–F12 can be diagnosed only on arms and hands.

### The legs barely move

| Largest joint range within one episode | min | median | p90 | max |
|---|---|---|---|---|
| Arm joints (rad) | 1.001 | 1.687 | 1.993 | 2.370 |
| Leg and waist joints (rad) | 0.010 | 0.028 | 0.056 | 0.598 |

Only 3 of the 40 episodes moved a leg or waist joint by more than 0.2 rad.

**Consequence.** Sensor faults on legs are detectable as *changes against a nearly constant signal*, which suits drift, bias onset, noise and freezing, but the data barely exercises them under motion. Report leg results separately from arm results.

### Arms follow their commands with a large, variable lag

| Per episode | min | median | p90 | max |
|---|---|---|---|---|
| Lag that best aligns command and measurement (frames at 30 Hz) | 5 | 8 | 11 | 14 |
| Same, in milliseconds | 167 | 267 | 367 | 467 |
| Arm residual p95, no lag compensation (rad) | 0.102 | 0.256 | 0.335 | 0.431 |
| Arm residual p95, lag compensated (rad) | 0.056 | 0.145 | 0.241 | 0.345 |

**Consequence.** A fixed threshold on the raw `command − measurement` difference would raise false alarms on healthy motion. The tracking rule must compensate for lag and be [calibrated per joint](../design/rules.md#calibration) on nominal data. Even compensated, per-joint p99 residuals reach 0.19–0.66 rad, so a subtle F12 may be hard to distinguish from teleoperated motion.

### Episodes are short

From the dataset's own metadata, the G1 lite set has 4,064 episodes, 1,779,287 frames and 247 tasks. That is **16.5 hours in total and about 14.6 s per episode on average**.

**Consequence.** A full cycle of detect, confirm, clear and return to healthy will often not fit in one episode, and a 60-minute run at 5× (NFR6) needs 5 hours of data. `ReplayAdapter` must [chain episodes](../design/ingestion.md#chaining-episodes) with an explicit boundary event.

### Timestamps are synthetic in the LeRobot formats

Timestamps there are simply frame index / 30 (measured jitter: at most 1 µs, which is rounding). Whether the raw `time` field has jitter, or is monotonic as DA3 assumes, has not been checked. Since it is a UNIX wall-clock value, monotonicity should not be taken for granted.

### Other checks

No NaN values appeared in the sampled joint and command data, which supports DA1 for those signals. It also means F5 is only ever exercised through injection.

## Summary: what this means for the fault model

| Area | Impact | Where it is handled |
|---|---|---|
| F9–F12 limited to arms and hands | Scenario S2 needs a change; DA2 needs narrowing | [RASD findings](../project/rasd-review.md), [fault coverage](../requirements/fault-catalogue.md#coverage-against-the-available-data) |
| Lag and residual size | Tracking rule compensates lag; thresholds are calibrated | [Rules](../design/rules.md) |
| Short episodes | Episode chaining; scenario timing changes | [Sources and ingestion](../design/ingestion.md) |
| Format choice | Raw for replay, lite for bulk training | [Open decisions](../project/decisions.md) |

**Next:** [Deliverables](deliverables.md)
