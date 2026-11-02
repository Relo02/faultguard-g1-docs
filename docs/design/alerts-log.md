# Alerts and event log

!!! proposed "Proposed"
    Implements FR39, FR41, FR42, FR44 and NFR14.

## AlertManager

The only component that raises alerts.

| Trigger | Action |
|---|---|
| `DiagnosticConfirmed` | Create `Alert`, publish `AlertRaised` (FR39) |
| `FaultLocalized` for a component with an open alert | Publish `AlertUpdated` if the hypotheses changed |
| `DiagnosticStateChanged` → ACKNOWLEDGED | Set `acknowledged_at`, publish `AlertAcknowledged` (FR41) |
| `DiagnosticStateChanged` with `evidence_present = false` | Publish `AlertUpdated`, marked "evidence no longer present" |

```python
@dataclass(frozen=True)
class Alert:
    alert_id: str
    diagnosis_id: str
    component: ComponentId
    region: str | None
    hypotheses: tuple[FaultHypothesis, ...]   # ranked, with confidence
    ambiguous_groups: tuple[str, ...]
    confirmed_at: TimeNs
    acknowledged_at: TimeNs | None = None
    evidence_present: bool = True
```

## EventLog

An append-only JSON Lines file per session, one event per line. It subscribes to all topics, except `TelemetryReceived` and `Heartbeat`, which are too frequent and are covered by the sample store and summarized by health snapshots.

```text
sessions/<session_id>/
├── session.json        config snapshot and hash, versions, seed, mode
├── events.jsonl        the event log (FR44)
├── samples.parquet     low-dimensional samples (FR42)
└── truth.json          ground truth, written by the harness only, if any
```

```json
{"type":"DiagnosticConfirmed","meta":{"event_id":"0190...","source_time":21834000000,
 "receive_time":21841000000,"publish_time":21952000000,"producer":"engine",
 "correlation_id":"win-a1-108","causes":["0190...","0190..."]},
 "diagnosis_id":"d-7","component":"joint.left_elbow",
 "hypotheses":[{"fault":"F2","confidence":0.71,"rank":1}],"evidence_ids":["0190..."]}
```

Writes go through a thread with batching, so disk latency doesn't touch the event loop. If the log's queue overflows, this is reported as `DataDiscarded`, and the affected session is marked non-traceable, rather than failing silently.

## SampleStore

Low-dimensional samples are written to Parquet, in batches, one row per sample: `stream, seq, source_time, receive_time, values, had_invalid`. Traceability needs samples, while bounded memory (NFR6) forbids holding them in RAM. Disk is the only place where both requirements hold. Perception data is referenced by its original path and not copied.

## TraceQuery

Serves the evidence trail for the UI (FR42) and the NFR14 check.

```python
class TraceQuery:
    def trail(self, alert_id: str) -> Trail:
        """Alert → confirmation → fused evidence → evidence → windows → sample refs."""

    def samples(self, ref: SampleRef) -> pa.Table: ...
```

During a live session an in-memory index covers the most recent events, up to a fixed maximum, and older queries fall back to the file. Memory therefore stays bounded.

## Testing

| Test | Verifies |
|---|---|
| Campaign log walk: every alert reaches at least one sample ref, and every ref resolves | NFR14 |
| Log can be replayed to rebuild final component states | FR44, log completeness |
| Alert contains all required fields | FR39 |
| Hypotheses update reaches the UI | S9 |
| Memory stable over a long run with trail queries | NFR6 |

**Next:** [Self-monitoring](self-monitoring.md)
