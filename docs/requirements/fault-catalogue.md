# Fault catalogue

!!! baseline "Baseline"
    The catalogue is RASD v0.1 Table 2.2. It is expected to grow (G4).

## The 19 fault types

| ID | Layer | Fault type | Observable effect | Injection point |
|---|---|---|---|---|
| F1 | Sensor | Encoder bias | Constant offset on a measured joint angle | Sample values |
| F2 | Sensor | Encoder drift | Offset on a measured joint angle growing over time | Sample values |
| F3 | Sensor | Encoder noise | Increased random noise on a measured joint angle | Sample values |
| F4 | Sensor | Frozen value | A sensor reports a constant value | Sample values |
| F5 | Sensor | Missing/NaN samples | Values missing or not numeric | Sample values |
| F6 | Sensor | IMU bias | Constant offset on accelerometer or gyroscope | Sample values |
| F7 | Sensor | IMU drift | Offset on IMU signals growing over time | Sample values |
| F8 | Sensor | Hand-pressure dropout | Tactile sensor readings drop to zero or vanish | Sample values |
| F9 | Joint/actuator | Stuck joint | Measurement frozen while commands change | Measured vs commanded angles |
| F10 | Joint/actuator | Partially responsive joint | Attenuated and lagged tracking of commands | Measured vs commanded angles |
| F11 | Joint/actuator | Oscillation/vibration | Periodic deviation around the command | Measured vs commanded angles |
| F12 | Joint/actuator | Excessive tracking error | Large persistent command/measurement error | Measured vs commanded angles |
| F13 | Communication | Delay | Samples received later than nominal | Stream |
| F14 | Communication | Packet loss | Samples missing from a stream | Stream |
| F15 | Communication | Out-of-order delivery | Samples received out of source order | Stream |
| F16 | Communication | Telemetry interruption | No samples for an extended interval | Stream |
| F17 | Monitoring system | Pipeline overload | Processing slower than incoming telemetry | Pipeline runtime |
| F18 | Monitoring system | Stalled component | A pipeline component stops its heartbeat | Pipeline runtime |
| F19 | Monitoring system | Clock skew | Source clocks of different streams diverge | Pipeline runtime |

## Coverage against the available data

!!! proposed "Proposed"
    The RASD leaves open which faults are mandatory for the prototype. This table proposes tiers, based on [what the data can support](../overview/dataset.md). *Core* covers all four layers and every scenario except the optional ones. *Planned* follows if the schedule holds. *Stretch* depends on signals not yet inspected. Cutting works upward from Stretch, as the [cut order](../project/risks.md#cut-order) allows.

| ID | Tier | Applies to | Main check | Observability notes |
|---|---|---|---|---|
| F1 | Planned | All joints | `step_change`, `tracking_error`, `range_limit` | Seen on arms as a residual offset. On legs, only a bias with a visible onset can be detected: there is no command to compare with. |
| F2 | **Core** | All joints | `drift`, `tracking_error` | On arms, residual slope. On legs, slope against a nearly constant signal; this works because legs barely move. |
| F3 | **Core** | All joints | `noise_level`, ML | Compare high-frequency energy with the calibrated nominal level. |
| F4 | **Core** | All joints, IMU, odometry | `frozen_value`, `cmd_meas_inconsistency` | Healthy encoders always vary slightly, so an exact repeat is a strong signal. Looks like F9 on arms. |
| F5 | **Core** | All signals | `missing_data` | No NaN in sampled data, so injection is the only source. |
| F6 | Stretch | IMU | `imu_consistency` | Needs raw or full format. Physical units still to verify. |
| F7 | Stretch | IMU | `imu_consistency`, `drift` | As F6. |
| F8 | Stretch | Hand pressure | `pressure_dropout` | Needs raw or full format. Reading ranges still to verify. |
| F9 | **Core** | Arms, hands | `cmd_meas_inconsistency`, `tracking_error` | Not diagnosable on legs or waist. |
| F10 | Planned | Arms, hands | `tracking_error`, ML | Must be distinguished from the nominal 167–467 ms lag. |
| F11 | **Core** | Arms, hands (residual); all joints (signal) | `oscillation`, skill `frequency_analysis` | Teleoperation is slow, so a higher-frequency band should separate cleanly; to be confirmed in calibration. |
| F12 | **Core** | Arms, hands | `tracking_error` | Nominal residuals are large: use a clearly large injected error at first. |
| F13 | Planned | All streams | `stream_health` | Requires arrival time to differ from source time. |
| F14 | **Core** | All streams | `stream_health` | Sequence gaps. |
| F15 | Planned | All streams | `stream_health`, reorder buffer | Sequence order against arrival. |
| F16 | **Core** | All streams | `stream_health` | Interruption of a few seconds must fit in one episode, or use chaining. |
| F17 | **Core** | Pipeline | Queue monitor | |
| F18 | **Core** | Pipeline | Heartbeat monitor | |
| F19 | Planned | Streams | Clock-skew detector | Injected by shifting source timestamps in the source wrapper. |

Some faults look identical in telemetry. S3 requires reporting both F4 and F9 when the data cannot tell them apart (FR26).

**Details:** [Rules](../design/rules.md) · [Fault injection](../design/fault-injection.md)
