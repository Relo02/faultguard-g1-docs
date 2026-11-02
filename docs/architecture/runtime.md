---
hide:
  - toc
---

# Runtime view

!!! proposed "Proposed"
    Refines the RASD's black-box sequence diagrams into internal components. Bus hops are shown as direct messages for readability.

## Detect, confirm, acknowledge, clear (S2)

```mermaid
sequenceDiagram
  autonumber
  participant SRC as Source
  participant ING as Ingestion
  participant WIN as Windower
  participant RUL as RuleEngine
  participant ML as MLRunner
  participant FUS as Fusion
  participant CL as Classify + Localize
  participant ENG as Engine
  participant ALR as AlertManager
  actor OP as Operator
  loop every sample
    SRC->>ING: TelemetrySample
    ING->>WIN: TelemetryReceived
  end
  loop every hop (0.2 s)
    WIN->>RUL: WindowReady
    WIN->>ML: WindowReady
    RUL->>FUS: EvidenceProduced
    ML->>FUS: EvidenceProduced
    FUS->>ENG: EvidenceFused(e)
    opt e ≥ θanomaly
      FUS->>CL: AnomalyDetected
      CL->>ENG: FaultLocalized(hypotheses)
    end
  end
  Note over ENG: T1: e ≥ θenter, HEALTHY to SUSPECTED
  ENG-->>OP: DiagnosticStateChanged
  Note over ENG: T3: e ≥ θconf held for Tconf
  ENG->>ALR: DiagnosticConfirmed
  ALR-->>OP: AlertRaised
  OP->>ALR: open evidence trail (TraceQuery)
  OP->>ENG: AcknowledgeRequested
  Note over ENG: T4: CONFIRMED to ACKNOWLEDGED
  ENG->>ALR: DiagnosticStateChanged
  ALR-->>OP: AlertAcknowledged
  Note over ENG: T5: e < θexit for Tclear, to CLEARED
  Note over ENG: T6: after Tdwell, to HEALTHY
```

## Latency budget for NFR1

NFR1 allows 2 s from the receive time of the last contributing sample to `DiagnosticConfirmed`, at 1×. T<sub>conf</sub> is not part of this budget: the last contributing sample is the one that completes it.

| Step | Default | Worst case at 1× |
|---|---|---|
| Reorder buffer holds sample until the watermark passes | W<sub>late</sub> = 100 ms | 100 ms |
| Waiting for the next window hop | Hop = 200 ms | 200 ms |
| Alignment across streams | Waits on the slowest active stream up to W<sub>late</sub> | 100 ms |
| Rule evaluation | Inline | < 20 ms (target) |
| ML evaluation including queueing | One window in flight, one queued | < 400 ms (target) |
| Fusion, engine, bus hops | | < 20 ms (target) |
| **Total** | | **≈ 840 ms** |

The margin of over a second is deliberate. It allows for a loaded laptop, and it also means the window parameters can grow during tuning. These targets must be measured in the event-bus spike; they are not measurements yet.

## Degraded link (S4)

```mermaid
sequenceDiagram
  participant SRC as Source + injector
  participant RB as ReorderBuffer
  participant HT as HealthTracker
  participant WIN as Windower
  participant RUL as RuleEngine
  participant FUS as Fusion
  participant ENG as Engine
  SRC->>RB: joint samples, out of order
  RB->>WIN: in source order
  SRC-xRB: sample beyond Wlate
  RB->>HT: late sample counted
  Note over HT: IMU loss ratio > ρdeg
  HT->>WIN: StreamHealthChanged(imu, DEGRADED)
  HT->>FUS: EvidenceProduced(stream.imu, F14)
  Note over HT: No IMU samples for Tstale
  HT->>WIN: StreamHealthChanged(imu, STALE)
  HT->>FUS: EvidenceProduced(stream.imu, F16, high score)
  WIN->>RUL: window with imu masked missing
  RUL->>FUS: EvidenceProduced(imu checks, DATA_MISSING)
  Note over FUS: Data-missing does not score against joints
  FUS->>ENG: EvidenceFused(stream.imu, high)
  FUS->>ENG: EvidenceFused(imu sensor, coverage=none)
  Note over ENG: stream.imu moves to CONFIRMED, imu sensor holds its state
```

## Overload (S5)

```mermaid
sequenceDiagram
  participant WIN as Windower
  participant Q as ML input queue
  participant ML as MLRunner
  participant BUS as Bus accounting
  participant MON as HealthMonitor
  participant FUS as Fusion
  participant ENG as Engine
  WIN->>Q: WindowReady, 25 per second at 5×
  Q->>ML: next window
  Note over Q: Queue full, coalesce: keep newest
  Q->>BUS: count discarded
  BUS->>MON: DataDiscarded(queue=ml, n=12, 1 s)
  MON->>FUS: EvidenceProduced(pipeline.ml, F17, score from drop ratio)
  FUS->>ENG: EvidenceFused(pipeline.ml, high)
  Note over ENG: pipeline.ml reaches CONFIRMED, operator is told coverage is reduced
  Note over Q: Replay back to 1×: drops stop, evidence falls, operator acknowledges, then cleared
```

## Stalled classifier (S9)

```mermaid
sequenceDiagram
  participant RUL as RuleEngine
  participant FUS as Fusion
  participant CLF as Classifier
  participant MON as HealthMonitor
  participant ENG as Engine
  participant ALR as AlertManager
  Note over CLF: Stall injected by harness wrapper
  CLF--xMON: no heartbeat
  Note over MON: Timeout exceeded
  MON->>FUS: EvidenceProduced(pipeline.classifier, F18)
  FUS->>ENG: EvidenceFused(pipeline.classifier)
  ENG->>ALR: DiagnosticConfirmed(pipeline.classifier)
  RUL->>FUS: EvidenceProduced(joint, still flowing)
  FUS->>ENG: EvidenceFused(joint)
  Note over ENG: A joint can still be CONFIRMED
  ENG->>ALR: DiagnosticConfirmed(joint, rule suggestions only)
```

## Guided diagnosis (S12)

```mermaid
sequenceDiagram
  actor OP as Operator
  participant UI as UI gateway
  participant ORC as Orchestrator
  participant PL as Planner
  participant SK as SkillRegistry
  participant FUS as Fusion
  participant ENG as Engine
  OP->>UI: "the left arm is vibrating"
  UI->>ORC: SymptomReported
  ORC->>PL: plan(symptom, catalogue, history)
  PL-->>ORC: run frequency_analysis, tracking_error, symmetry
  loop until ranked or max iterations
    ORC->>SK: run skill (read-only view)
    SK-->>ORC: SkillResult
    ORC->>PL: plan(results so far)
    PL-->>ORC: next skills, or ranked hypotheses
  end
  ORC->>FUS: EvidenceProduced(kind=GUIDED, capped score)
  FUS->>ENG: EvidenceFused
  Note over ENG: May become SUSPECTED, confirmation still needs the state machine
  ORC->>UI: GuidedDiagnosisCompleted
  UI-->>OP: hypotheses, skills, results, justification
```

## Evaluation campaign (S11)

```mermaid
sequenceDiagram
  actor TE as Test engineer
  participant CR as CampaignRunner
  participant SL as ScenarioLoader
  participant GT as GroundTruth file
  participant PB as PipelineBuilder
  participant LOG as EventLog
  participant EV as Evaluator
  TE->>CR: campaign.yaml
  loop mode × scenario × episode × seed
    CR->>SL: load(scenario, seed)
    SL-->>CR: injectors
    SL->>GT: truth for this run
    CR->>PB: build(mode, FaultInjectingSource, VirtualClock)
    PB-->>CR: pipeline
    CR->>PB: run to completion
    PB->>LOG: events
  end
  CR->>EV: evaluate(logs, truth)
  EV-->>TE: report.json + summary
```

**Next:** [Concurrency and backpressure](concurrency.md)
