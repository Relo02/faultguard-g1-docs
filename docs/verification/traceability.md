# Traceability

!!! proposed "Proposed"
    Input for Design Document chapter 4. `tools/check_traceability.py` runs in CI, and fails if any requirement from the [functional](../requirements/functional.md) or [non-functional](../requirements/non-functional.md) pages is missing from this page.

## Functional requirements

| ID | Design elements | Test location |
|---|---|---|
| FR1 | `TelemetrySource`, adapters | `tests/unit/sources`, `tests/architecture` |
| FR2 | `StreamIngestor` | `tests/unit/ingestion` |
| FR3 | `StreamIngestor`, `TelemetrySample` | `tests/unit/ingestion` |
| FR4 | `TimeAligner` | `tests/unit/ingestion` |
| FR5 | `ReorderBuffer` | `tests/unit/ingestion` (property) |
| FR6 | `ReorderBuffer`, `HealthSnapshot` | `tests/unit/ingestion` (property) |
| FR7 | `StreamHealthTracker`, `TimeAligner` masks | `tests/unit/ingestion`, S4 |
| FR8 | `TelemetrySample`, `MissingDataRule`, `FaultLocalizer` | `tests/unit/checks` |
| FR9 | `ReplayAdapter` | `tests/unit/sources` |
| FR10 | `StreamSplitter` | `tests/unit/sources` |
| FR11 | `ScenarioLoader`, scenario schema | `tests/unit/harness` |
| FR12 | `InjectorFactory`, `load_plugin` | `tests/unit/harness`, S10 |
| FR13 | `ValueInjector`, `StreamInjector`, `StageFault` | `tests/unit/harness` |
| FR14 | `CompositeInjector`, `FaultInjectingSource` | `tests/unit/harness`, S8 |
| FR15 | `GroundTruthRecorder`, import contract | `tests/architecture` |
| FR16 | Per-injector generators | `tests/unit/harness` |
| FR17 | `Rule` subclasses, `StreamHealthTracker` | `tests/unit/checks` |
| FR18 | `MLDetector`, `MLDetectorRunner` | `tests/unit/checks`, `tests/integration` |
| FR19 | `Evidence`, `Window.correlation_id` | `tests/unit/checks`, log walk |
| FR20 | `RuleEngine`, `AlertManager`, independence contract | `tests/architecture` |
| FR21 | `EvidenceFusion`, `FusionPolicy` | `tests/unit/fusion` |
| FR22 | `EvidenceFusion`, UI indicator | `tests/unit/fusion`, S7 |
| FR23 | `PipelineBuilder` mode | `tests/integration` |
| FR24 | `checks.yaml`, `RuleEngine` | `tests/unit/config` |
| FR25 | `FaultClassifier`, `HypothesisRanker` | `tests/unit/diagnosis` |
| FR26 | `FaultClassifier`, confusable groups | `tests/unit/diagnosis`, S3 |
| FR27 | `FaultLocalizer`, `RobotModel` | `tests/unit/diagnosis` |
| FR28 | `FaultLocalizer`, `EvidenceStatus`, `Coverage` | `tests/unit/diagnosis`, S4 |
| FR29 | `ComponentFsm` | `tests/unit/diagnosis` |
| FR30 | T1 | `tests/unit/diagnosis` |
| FR31 | T3, `DiagnosticConfirmed` | `tests/unit/diagnosis` (property) |
| FR32 | T2 | `tests/unit/diagnosis` |
| FR33 | T4 as CONFIRMED's only exit | `tests/unit/diagnosis` (property) |
| FR34 | T4, `AcknowledgeRequested` | `tests/unit/diagnosis` |
| FR35 | T5, T6, T7 | `tests/unit/diagnosis` |
| FR36 | `FsmParams`, `fsm.yaml` | `tests/unit/config` |
| FR37 | `RegionAggregator` | `tests/unit/diagnosis` |
| FR38 | UI gateway, `SessionFactory` | `tests/integration/ui` |
| FR39 | `AlertManager`, `Alert` | `tests/unit/alerts` |
| FR40 | UI main view, `/ws/events` | `tests/integration/ui` |
| FR41 | `AlertManager`, `/api/alerts/{id}/ack` | `tests/integration/ui` |
| FR42 | `TraceQuery`, `SampleStore`, evidence panel | `tests/integration/ui` |
| FR43 | `HealthSnapshot`, UI health panel | `tests/unit/monitoring` |
| FR44 | `EventLog` | `tests/integration/persistence` |
| FR45 | `StageRunner`, `HealthMonitor` | `tests/unit/monitoring`, S9 |
| FR46 | `BoundedQueue`, `EventBus` | `tests/unit/kernel` (property) |
| FR47 | `DataDiscarded`, `HealthMonitor` | `tests/unit/monitoring`, S5 |
| FR48 | `ClockSkewDetector` | `tests/unit/monitoring` |
| FR49 | `/api/symptoms`, `SymptomReported` | `tests/integration/ui` |
| FR50 | `DiagnosisOrchestrator`, `DiagnosisPlanner` | `tests/unit/guided` |
| FR51 | `SkillRegistry`, five skills | `tests/unit/guided` |
| FR52 | `TelemetryView` | `tests/architecture` |
| FR53 | `DiagnosisOrchestrator`, `guided_cap` | `tests/unit/fusion`, `tests/architecture` |
| FR54 | `RuleBasedPlanner` | `tests/unit/guided` |
| FR55 | `GuidedDiagnosisCompleted`, UI panel | `tests/integration/ui` |
| FR56 | `on_planner_failure` | `tests/unit/guided` |
| FR57 | `Evaluator` | `tests/unit/harness` |
| FR58 | `CampaignRunner`, `ReportWriter` | `tests/integration/harness`, S11 |
| FR59 | `Evaluator`, scripted symptoms | `tests/unit/harness` |
| FR60 | `CampaignRunner`, `ReportWriter` | `tests/integration/harness` |

## Non-functional requirements

| ID | Design elements | Verification |
|---|---|---|
| NFR1 | Latency budget, source-time timers | Real-time campaign, log timestamps |
| NFR2 | `/ws/events`, bounded client queue | Instrumented UI timing |
| NFR3 | `BoundedQueue`, overflow policies | Load tests at 1×, 2×, 5× |
| NFR4 | `ReorderBuffer`, masks, `StageRunner` | Injection suite F5, F13–F16 |
| NFR5 | `StageRunner`, rule isolation, worker process | Failing check, F18 |
| NFR6 | Bounded queues, disk-based store, trail limit | Memory profile over a long chained run |
| NFR7 | `rearmed` guard, hysteresis, T2 dwell | Property test, S6 |
| NFR8 | `Evaluator`, `CampaignRunner` | Campaign report |
| NFR9 | `Evaluator` | Campaign report |
| NFR10 | `load_plugin`, `ValueInjector` | `tests/architecture/test_extension.py`, diff, demo |
| NFR11 | `load_plugin`, `DiagnosticCheck` | `tests/architecture/test_extension.py`, diff, demo |
| NFR12 | `SkillRegistry`, `DiagnosticSkill` | Commit diff |
| NFR13 | `TelemetrySource` | Commit diff |
| NFR14 | `Event.causes`, `SampleRef`, `TraceQuery` | Automated log walk |
| NFR15 | `VirtualClock`, seeds, `deterministic` mode | Repeated runs compared |
| NFR16 | `LlmClient`, `StubLlmClient` | Tests without network |
| NFR17 | `TelemetrySource`, `TelemetryView`, no write operations | Inspection, architecture test |
| NFR18 | UI main view | Walkthrough |
| NFR19 | State display table | Inspection |
| NFR20 | Stack without GPU, ML worker | Install on team machines |

## Goals to scenarios

| Goal | Scenarios |
|---|---|
| G1 | S1, S2, S3, S8 |
| G2 | S1, S6, S7 |
| G3 | S4, S5, S9 |
| G4 | S10 |
| G5 | S2, S7 |
| G6 | S8, S11 |
| G7 | S12 |
