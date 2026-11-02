# Operator UI

!!! proposed "Proposed"
    Implements FR38–FR43, FR49, FR55 and NFR2, NFR18, NFR19. Input for Design Document chapter 3, which also needs proper mockups. UI polish is on the [cut list](../project/risks.md#cut-order), but the functions below are not.

## Main view

```text
┌ FaultGuard-G1 ───────────────────────────────────────────────────────────────┐
│ Source [Replay ▾]  Episode [push_a_button/3 ▾]  Scenario [s2_drift ▾]        │
│ Rate [1× ▾]   [▶ Start] [⏸ Pause] [■ Stop]     Session a1 · 00:42 · HYBRID   │
├───────────────────────────────┬──────────────────────────────────────────────┤
│ BODY REGIONS                  │ ALERTS                                       │
│  ● Left arm    CONFIRMED      │ ▲ CONFIRMED 00:39  Left elbow                │
│  ○ Right arm   HEALTHY        │   F2 Encoder drift            0.71           │
│  ○ Left leg    HEALTHY        │   F12 Excessive tracking      0.22           │
│  ◐ Right leg   SUSPECTED ⚑    │   [Evidence]  [Acknowledge]                  │
│  ○ Waist       HEALTHY        │                                              │
│  ○ Left hand   HEALTHY        │ ▲ CONFIRMED 00:31  Stream imu                │
│  ○ Right hand  HEALTHY        │   F16 Telemetry interruption  0.98           │
│                               │   [Evidence]  [Acknowledge]                  │
│ ▼ Left arm                    ├──────────────────────────────────────────────┤
│    shoulder pitch  HEALTHY    │ ASK ABOUT A SYMPTOM                          │
│    elbow           CONFIRMED  │ [ the left arm is vibrating             ][→] │
│    wrist roll      SUSPECTED  │ Planner: rule-based · 2 skills · 1 iteration │
├───────────────────────────────┴──────────────────────────────────────────────┤
│ SYSTEM HEALTH                                                                │
│ Streams  joint.arm ● ACTIVE   imu ✕ STALE   odometry ● ACTIVE                │
│ Queues   rules 2/16   ml 4/4 ▲   evidence 12/1024   dropped 37               │
│ Stages   all alive · classifier ✕ no heartbeat 4 s                           │
└──────────────────────────────────────────────────────────────────────────────┘
```

`⚑` is the evidence-conflict indicator (FR22).

## State display

Each state uses a distinct text label, colour and symbol, consistent across views (NFR19), so that colour is never the only signal.

| State | Label | Symbol | Colour |
|---|---|---|---|
| Healthy | <span class="st st-h">HEALTHY</span> | ○ | Green |
| Suspected | <span class="st st-s">SUSPECTED</span> | ◐ | Amber |
| Confirmed | <span class="st st-c">CONFIRMED</span> | ● | Red |
| Acknowledged | <span class="st st-a">ACKNOWLEDGED</span> | ◉ | Purple |
| Cleared | <span class="st st-l">CLEARED</span> | ◌ | Blue |

Extra markers: `⚑` evidence conflict; "no coverage" when evidence is missing; "evidence no longer present" on a latched alert; "recurrent" after T7.

## Evidence trail

**[Evidence]** opens a side panel (one interaction, NFR18), containing the timeline of fused evidence against the thresholds, the state transitions, a table of checks with their scores and details, any conflict, and the telemetry plot for the sample range. For a tracking fault it overlays command and measurement.

**[Acknowledge]** is a single click (NFR18). It requires no dialog, since the action is safe and reversible by the state machine.

## Gateway API

The UI gateway only translates between HTTP or WebSocket and the bus. It has no diagnostic logic.

| Method | Path | Purpose | Requirement |
|---|---|---|---|
| `GET` | `/api/catalog` | Sources, episodes, scenarios | FR38 |
| `POST` | `/api/session` | Start with source, episode, scenario, rate | FR38 |
| `POST` | `/api/session/{id}/pause`, `/resume`, `/stop` | Control | FR38 |
| `POST` | `/api/alerts/{id}/ack` | Acknowledge | FR41 |
| `GET` | `/api/alerts/{id}/trail` | Evidence trail | FR42 |
| `GET` | `/api/samples` | Samples by stream and range | FR42 |
| `POST` | `/api/symptoms` | Report a symptom | FR49 |
| `WS` | `/ws/events` | Push of state, alert, health and guided events | FR40, FR43, FR55, NFR2 |

!!! note "Scenario selection and the harness boundary"
    FR38 lets the operator pick a fault scenario. To keep `faultguard` independent of the harness, the application started by `faultguard-harness run` registers its scenario catalogue with the gateway, through a plain `SessionFactory` interface. The Diagnostic System itself offers only a session factory without faults.

## Timing (NFR2)

Each WebSocket message carries the event's `publish_time`. The client records its receive and paint times, and reports them back in test mode. The WebSocket queue is bounded and coalesces health snapshots, but never coalesces alerts. A UI that is slow or disconnected can't block the pipeline, since it is only another subscriber.

## Testing

| Test | Verifies |
|---|---|
| API tests: start, pause, stop, ack, trail | FR38, FR41, FR42 |
| WebSocket pushes state within budget under load | NFR2 |
| Slow WebSocket client doesn't affect the pipeline | NFR5 |
| Scripted walkthrough, from main view to evidence and to ack | NFR18 |
| Every state rendered with colour and label | NFR19 |

**Next:** [Configuration](configuration.md)
