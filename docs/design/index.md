# Low-level design

!!! proposed "Proposed"
    This section is the concrete design to implement against. It proposes types, algorithms and default parameters. **Parameter values are starting points to be tuned**, and code samples show intended interfaces, not finished code. Once reviewed, this becomes the class view of the Design Document (§2B).

## How to use this section

Each page follows the same order: what the component must do, its interface, its algorithm, its defaults, and how to test it. Requirements are cited, so a page can be checked against the RASD.

| Page | Implements | Increment |
|---|---|---|
| [Code layout](layout.md) | Packages, dependency rules | 1 |
| [Domain types](domain-types.md) | Events and value objects | 1 |
| [Event bus](event-bus.md) | Bus, queues, runner | 1 |
| [Sources and ingestion](ingestion.md) | FR1–FR10 | 1 |
| [Fault injection](fault-injection.md) | FR11–FR16 | 2 |
| [Rules](rules.md) | FR17, FR19, FR20, FR24 | 2 |
| [ML detectors](ml.md) | FR18, FR23 | 3 |
| [Evidence fusion](fusion.md) | FR21, FR22 | 3 |
| [Classification and localization](classify-localize.md) | FR25–FR28 | 3 |
| [Diagnostic engine](diagnostic-engine.md) | FR29–FR37 | 4 |
| [Alerts and event log](alerts-log.md) | FR39, FR41, FR42, FR44 | 4 |
| [Self-monitoring](self-monitoring.md) | FR43, FR45–FR48 | 4 |
| [Operator UI](ui.md) | FR38–FR43 | 5 |
| [Guided diagnosis](guided.md) | FR49–FR56 | 5 |
| [Configuration](configuration.md) | FR11, FR12, FR24, FR36 | All |

Increments refer to the [project plan](../project/roadmap.md).

## Default parameters

Single reference for values used across the pages.

| Parameter | Symbol | Default | Basis |
|---|---|---|---|
| Lateness window | W<sub>late</sub> | 100 ms | 3 frames at 30 Hz |
| Staleness timeout | T<sub>stale</sub> | 500 ms | 15 missed frames |
| Window length | | 1.0 s (30 frames) | Long enough to see the 167–467 ms lag |
| Window hop | | 0.2 s (6 frames) | Fits the latency budget |
| Enter threshold | θ<sub>enter</sub> | 0.5 | |
| Exit threshold | θ<sub>exit</sub> | 0.3 | Hysteresis gap of 0.2 |
| Confirm threshold | θ<sub>conf</sub> | 0.7 | |
| Dwell time | T<sub>dwell</sub> | 2.0 s | Must fit inside an episode |
| Confirm time | T<sub>conf</sub> | 1.0 s | 5 hops |
| Clear time | T<sub>clear</sub> | 3.0 s | |
| Conflict margin | | 0.4 | |
| Hypothesis threshold | θ<sub>hyp</sub> | 0.2 | |
| Heartbeat period | | 1 s | |
| Heartbeat timeout | | 3 s | |
| Stream loss thresholds | ρ<sub>deg</sub>, ρ<sub>ok</sub> | 0.1, 0.02 | Over a 2 s window |
| Max delay | d<sub>max</sub> | 300 ms | |
| Clock-skew tolerance | | 100 ms | |
| Guided iterations, timeout | | 4, 20 s | |

!!! warning "Episode length constrains the timers"
    Typical detect-to-clear time is hop + T<sub>conf</sub> + acknowledgement + T<sub>clear</sub> + T<sub>dwell</sub>, or about 6 s plus the operator's reaction. With episodes around 14.6 s, longer timers would require chaining episodes for every test.
