# Code layout

!!! proposed "Proposed"

The repository has one directory per deliverable, as the guideline requires.

```text
SE4A_<names>/
├── D1_RASD/
├── D2_DesignDocument/
└── D3_Implementation/
    ├── pyproject.toml
    ├── README.md                   installation and run instructions
    ├── configs/                    session, checks, fsm, faults, robot model
    ├── scenarios/                  fault scenarios, one per RASD scenario
    ├── campaigns/
    ├── models/                     trained artifacts + model cards
    ├── src/
    │   ├── faultguard/             the Diagnostic System
    │   │   ├── kernel/             domain types, events, bus, clock
    │   │   │   ├── types.py
    │   │   │   ├── events.py
    │   │   │   ├── bus.py
    │   │   │   ├── runner.py
    │   │   │   └── clock.py
    │   │   ├── robot/              RobotModel: joints, regions, limits
    │   │   ├── sources/            TelemetrySource, ReplayAdapter, SimAdapter, G1Adapter
    │   │   ├── ingestion/          ingestor, reorder, health, align, window
    │   │   ├── checks/
    │   │   │   ├── base.py         DiagnosticCheck
    │   │   │   ├── engine.py       RuleEngine
    │   │   │   ├── rules/          one module per rule
    │   │   │   └── ml/             feature extraction, runner, detectors
    │   │   ├── fusion/             EvidenceFusion, FusionPolicy
    │   │   ├── diagnosis/          classifier, localizer, engine, fsm
    │   │   ├── alerts/             AlertManager
    │   │   ├── monitoring/         HealthMonitor, skew, watchdog
    │   │   ├── guided/             orchestrator, planners, skills, llm client
    │   │   ├── persistence/        EventLog, SampleStore, TraceQuery
    │   │   ├── ui/                 FastAPI gateway, static assets
    │   │   ├── config/             Pydantic schemas, plugin loader
    │   │   └── app/                PipelineBuilder, CLI
    │   └── faultguard_harness/     the Validation Harness
    │       ├── injectors/          one module per injector family
    │       ├── scenario.py         ScenarioLoader, InjectorFactory
    │       ├── source.py           FaultInjectingSource
    │       ├── stage_faults.py     StallingStage, SlowStage
    │       ├── ground_truth.py
    │       ├── campaign.py
    │       ├── evaluation.py
    │       ├── report.py
    │       ├── training.py         fit and calibrate
    │       └── cli.py
    └── tests/
        ├── unit/
        ├── integration/
        ├── scenarios/              one test per RASD scenario
        └── architecture/           dependency and extensibility tests
```

## Dependency rules

Enforced by `import-linter` in CI, which makes architectural violations build failures.

```toml
[tool.importlinter]
root_packages = ["faultguard", "faultguard_harness"]

[[tool.importlinter.contracts]]
name = "The Diagnostic System never imports the harness (FR15)"
type = "forbidden"
source_modules = ["faultguard"]
forbidden_modules = ["faultguard_harness"]

[[tool.importlinter.contracts]]
name = "Layers"
type = "layers"
layers = [
  "faultguard.app",
  "faultguard.ui",
  "faultguard.persistence | faultguard.sources",
  "faultguard.guided | faultguard.monitoring | faultguard.alerts",
  "faultguard.diagnosis | faultguard.fusion | faultguard.checks | faultguard.ingestion",
  "faultguard.config | faultguard.robot",
  "faultguard.kernel",
]

[[tool.importlinter.contracts]]
name = "Stages share nothing directly"
type = "independence"
modules = [
  "faultguard.ingestion", "faultguard.checks", "faultguard.fusion",
  "faultguard.diagnosis", "faultguard.alerts", "faultguard.monitoring",
]
```

## The composition root

`PipelineBuilder` in `faultguard.app` is the only place that knows every component. It reads configuration, instantiates stages and registers subscriptions. The harness calls it with a wrapped source and optional stage wrappers, so that the Diagnostic System has no idea it is under test.

```python
pipeline = PipelineBuilder(config).build(
    source=FaultInjectingSource(ReplayAdapter(cfg.replay), injectors, truth_recorder),
    clock=VirtualClock(),
    stage_wrappers={"classifier": StallingStage(after=seconds(10))},
)
await pipeline.run()
```

**Next:** [Domain types](domain-types.md)
