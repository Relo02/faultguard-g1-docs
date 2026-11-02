---
hide:
  - toc
---

# Domain model

!!! baseline "Baseline"
    From RASD v0.1 §2.2. The domain model describes concepts of the problem, independently of design decisions. Design classes are under [low-level design](../design/index.md).

## Robot and telemetry

A `Robot` is composed of `BodyRegion`s (left and right arm, left and right leg, waist, left and right hand), each composed of `Joint`s with position limits. The robot carries `Sensor`s; a joint encoder measures exactly one joint. Each sensor produces a `TelemetryStream` with a nominal rate; command streams are produced by the robot's controller rather than a sensor. A stream is a sequence of `TelemetrySample`s, each a `Measurement` or a `JointCommand`. A `TelemetrySource` provides the streams of one robot, and can be a replay of an `Episode` of a `Dataset`, a simulation or the live robot.

```mermaid
classDiagram
  class Robot {
    model : String
  }
  class BodyRegion {
    name : RegionName
  }
  class Joint {
    name : String
    lowerLimit : Angle
    upperLimit : Angle
  }
  class Sensor {
    kind : SensorKind
    nominalRate : Frequency
  }
  class TelemetryStream {
    signal : String
    nominalRate : Frequency
  }
  class TelemetrySample {
    sequenceNo : Integer
    sourceTime : Timestamp
    receiveTime : Timestamp
  }
  class Measurement {
    value : Value
  }
  class JointCommand {
    targetPosition : Angle
    feedForwardTorque : Torque
  }
  class TelemetrySource {
    kind : SourceKind
  }
  class Episode {
    taskDescription : String
    duration : Duration
  }
  class Dataset {
    name : String
    licence : String
  }
  class SensorKind {
    <<enumeration>>
    JOINT_ENCODER
    IMU
    ODOMETRY
    HAND_PRESSURE
    RGBD_CAMERA
    LIDAR
  }
  class SourceKind {
    <<enumeration>>
    REPLAY
    SIMULATION
    LIVE_ROBOT
  }
  Robot "1" *-- "1..*" BodyRegion
  BodyRegion "1" *-- "1..*" Joint
  Robot "1" --> "1..*" Sensor
  Sensor "0..1" --> "0..*" TelemetryStream : produces
  Sensor "0..1" --> "0..1" Joint : measures
  TelemetrySource "1" --> "1..*" TelemetryStream : provides
  TelemetryStream "1" *-- "0..*" TelemetrySample
  TelemetrySample <|-- Measurement
  TelemetrySample <|-- JointCommand
  JointCommand "0..*" --> "1" Joint : targets
  TelemetrySource "0..*" --> "0..1" Episode : replays
  Dataset "1" *-- "1..*" Episode
```

!!! note
    The cardinality on `Sensor`–`Joint` is simplified here: the RASD figure shows a joint encoder measuring exactly one joint. In the G1 data, `JointCommand` exists for arm and hand joints only, and `feedForwardTorque` for arm joints only; see [Telemetry data](../overview/dataset.md).

## Evidence and diagnosis

A `MonitoringSession` uses one telemetry source and runs in hybrid or rules-only mode. A `MonitoredComponent` is anything whose health is tracked: a joint, body region, sensor, stream, or a stage of the monitoring pipeline. `DiagnosticCheck`s (`Rule`, `MLDetector`, `DiagnosticSkill`) produce `Evidence` about a component over a time window, possibly suggesting a `FaultType`. When rule-based and ML evidence disagree, an `EvidenceConflict` relates them. Each component has a `Diagnosis`, supported by evidence and holding ranked `FaultHypothesis` entries. A confirmed diagnosis raises an `Alert`, which an `Operator` acknowledges.

```mermaid
classDiagram
  class MonitoringSession {
    startTime : Timestamp
    replayRate : Real
    mode : DetectionMode
  }
  class Diagnosis {
    state : DiagnosticState
    since : Timestamp
  }
  class FaultHypothesis {
    confidence : 0..1
    rank : Integer
  }
  class FaultType {
    id : String
    name : String
    layer : FaultLayer
  }
  class Evidence {
    score : 0..1
    window : TimeInterval
    time : Timestamp
    correlationId : ID
  }
  class MonitoredComponent {
    id : String
  }
  class DiagnosticCheck {
    name : String
    enabled : Boolean
  }
  class Rule {
    condition : Expression
  }
  class MLDetector {
    model : String
  }
  class DiagnosticSkill {
    description : String
  }
  class EvidenceConflict {
    detectedAt : Timestamp
    margin : Real
  }
  class Alert {
    raisedAt : Timestamp
    acknowledgedAt : Timestamp
  }
  class Operator {
    name : String
  }
  class TelemetrySource
  class DiagnosticState {
    <<enumeration>>
    HEALTHY
    SUSPECTED
    CONFIRMED
    ACKNOWLEDGED
    CLEARED
  }
  class FaultLayer {
    <<enumeration>>
    SENSOR
    JOINT_ACTUATOR
    COMMUNICATION
    MONITORING_SYSTEM
  }
  class DetectionMode {
    <<enumeration>>
    HYBRID
    RULES_ONLY
  }
  MonitoringSession "0..*" --> "1" TelemetrySource : uses
  MonitoringSession "1" *-- "0..*" Diagnosis
  Diagnosis "0..*" --> "1" MonitoredComponent : of
  Diagnosis "0..1" --> "0..*" FaultHypothesis : ranks
  Diagnosis "0..*" --> "0..*" Evidence : supported by
  Diagnosis "1" --> "0..*" Alert : raises
  Alert "0..*" --> "0..1" Operator : acknowledges
  FaultHypothesis "0..*" --> "1" FaultType : of type
  Evidence "0..*" --> "1" MonitoredComponent : concerns
  Evidence "0..*" --> "0..1" FaultType : suggests
  Evidence "0..*" --> "1" DiagnosticCheck : produced by
  EvidenceConflict "0..*" --> "2" Evidence : between
  DiagnosticCheck <|-- Rule
  DiagnosticCheck <|-- MLDetector
  DiagnosticCheck <|-- DiagnosticSkill
```

`MonitoredComponent` is specialized by `Joint`, `BodyRegion`, `Sensor`, `TelemetryStream`, and `PipelineComponent` (a stage of the monitoring system itself).

## Fault injection, evaluation and guided diagnosis

A `FaultScenario` is composed of `InjectedFault`s, each of a fault type and targeting a monitored component over a time interval; it is the ground truth of a session. An `EvaluationReport` summarizes sessions in one detection mode, with one `FaultClassMetrics` per fault type. An operator submits a `SymptomReport`, which starts a `GuidedDiagnosis` that uses a planner, runs skills, and produces evidence and ranked hypotheses.

```mermaid
classDiagram
  class FaultScenario {
    name : String
    seed : Integer
  }
  class InjectedFault {
    onset : Timestamp
    duration : Duration
    parameters : Map
  }
  class EvaluationReport {
    mode : DetectionMode
    createdAt : Timestamp
  }
  class FaultClassMetrics {
    detectionRate : 0..1
    falseAlarmRate : Real
    meanDetectionDelay : Duration
    localizationAccuracy : 0..1
  }
  class SymptomReport {
    text : String
    time : Timestamp
  }
  class GuidedDiagnosis {
    planner : PlannerKind
    maxIterations : Integer
    iterations : Integer
  }
  class PlannerKind {
    <<enumeration>>
    LLM_VLM
    RULE_BASED
  }
  class MonitoringSession
  class MonitoredComponent
  class FaultType
  class Operator
  class DiagnosticSkill
  class FaultHypothesis
  class Evidence
  FaultScenario "1" *-- "1..*" InjectedFault
  FaultScenario "0..1" --> "0..*" MonitoringSession : applies
  InjectedFault "0..*" --> "1" MonitoredComponent : targets
  InjectedFault "0..*" --> "1" FaultType : of type
  MonitoringSession "1..*" <-- "0..*" EvaluationReport : summarizes
  EvaluationReport "1" *-- "1..*" FaultClassMetrics
  FaultClassMetrics "0..*" --> "1" FaultType : for
  Operator "1" --> "0..*" SymptomReport : submits
  SymptomReport "1" --> "1" GuidedDiagnosis : triggers
  GuidedDiagnosis "0..*" --> "1..*" DiagnosticSkill : runs
  GuidedDiagnosis "0..1" --> "0..*" FaultHypothesis : ranks
  GuidedDiagnosis "1" --> "0..*" Evidence : produces
```
