# Assumptions, dependencies and constraints

!!! baseline "Baseline"
    From RASD v0.1 §2.6.

## Domain assumptions

These are assumed to hold in the world. The requirements guarantee the goals only if they do. The last column records what checking the data has shown so far.

| ID | Assumption | Status after [data check](../overview/dataset.md) |
|---|---|---|
| DA1 | The G1 recordings of Humanoid Everyday represent nominal behaviour; any real anomaly they contain is rare and is treated as noise in the evaluation. *Open: screen the selected episodes for obvious anomalies.* | No NaN in sampled joint and command data. Screening still to do. |
| DA2 | The recorded commanded joint targets are those sent to the robot's low-level controller, and under nominal conditions the measured joint angles follow them with a bounded tracking error. | **Holds only for arms and hands**; there are no leg commands. `sol_q` is the inverse-kinematics solution; whether it equals the value sent to the controller is unconfirmed. Lag is 167–467 ms. |
| DA3 | Every sample carries a source timestamp from a monotonic robot clock. | **Unverified.** Raw `time` is a UNIX timestamp; LeRobot timestamps are synthetic. |
| DA4 | The nominal rate of every stream is known (30 Hz in the dataset). | Holds at the dataset level (`fps` = 30). |
| DA5 | The joint limits and the physical ranges of the G1 sensors are known from the manufacturer's specifications. | To be collected and stored in the robot model. |
| DA6 | The injected faults reproduce the observable effects of the corresponding real faults closely enough to evaluate the architecture and to compare the checks. | Accepted; cannot be checked without hardware. |
| DA7 | During a session the operator attends the user interface and acknowledges alerts deliberately. | Accepted. |
| DA8 | The LLM/VLM service may be unavailable, slow or wrong; its answers are treated as untrusted evidence. | Accepted; see [guided diagnosis](../design/guided.md). |
| DA9 | During timing and load tests, the monitoring computer does not run other heavy workloads. | Accepted. |
| DA10 | A monitoring session observes exactly one robot. | Accepted. |

## Dependencies

- The Humanoid Everyday dataset: its availability, data format and licence terms.
- The MuJoCo simulator and a G1 model, for the optional simulation source.
- An LLM/VLM service and network access to it, for the LLM/VLM planner of guided diagnosis.
- Access to a Unitree G1, only for the optional live source.
- Machine-learning libraries providing the anomaly detectors, for example Isolation Forest and Random Forest.

## Constraints

- **Read-only system.** FaultGuard-G1 only observes; it performs no recovery and no actuation of the robot.
- **Fault labels from injection only.** The recordings are nominal, so every labelled fault comes from controlled injection. No physical fault is created on the hardware.
- **Available signals.** Only signals present in the dataset can be used; in particular there are no motor temperatures or currents.
- **Architecture agreed in the proposal.** Components communicate only through immutable domain events and share no mutable state.
- **Project constraints.** A group of three students, three months from the agreed starting date.
