# Classification and localization

!!! proposed "Proposed"
    Implements FR25–FR28.

## FaultClassifier

Triggered by `AnomalyDetected`, the classifier produces a ranked list from the fault catalogue. Rankers are a Strategy.

```python
class HypothesisRanker(Protocol):
    def rank(self, anomaly: AnomalyDetected, context: RankingContext) -> list[Hypothesis]: ...
```

| Ranker | Mode | Method |
|---|---|---|
| `SuggestionVoting` | Rules-only and hybrid | Confidence for fault *f* is the normalized sum of scores of evidence suggesting *f*, with weights from configuration |
| `RandomForestRanker` | Hybrid | Class probabilities from the trained model |
| `BlendedRanker` | Hybrid default | Weighted average of the two |

`SuggestionVoting` needs no model, so a new fault type with a new rule that suggests it is ranked immediately, with no retraining (NFR10). The Random Forest learns the new fault only when retrained. That counts as data rather than code, and the demo should say so openly.

### Honest ambiguity

Every hypothesis with confidence ≥ θ<sub>hyp</sub> is reported (FR26), not just the best one. For S3 the catalogue records that F4 and F9 are confusable, so `RankingContext` can raise a "not separable" flag. Such groups are defined in configuration:

```yaml
confusable_groups:
  - {faults: [F4, F9], reason: "A frozen measurement looks identical from telemetry alone"}
```

If several members of a group are present, the UI says that the telemetry can't distinguish them, which is more useful than a confidence that looks like a decision.

## FaultLocalizer

Takes `FaultClassified` and publishes `FaultLocalized`. It answers two questions.

**Where?** From the `RobotModel`: joint → region, sensor → region if applicable, stream or pipeline stage → no region (FR27).

**Is the fault really there?** It applies attribution rules, in order:

| # | Situation | Result |
|---|---|---|
| 1 | Stream of this joint is STALE or DEGRADED, and the joint's evidence comes only from missing or irregular data | Suppress the joint hypothesis; the stream's own evidence covers it (FR28) |
| 2 | Evidence is `missing_data` with samples present (NaN inside an arriving sample) | Sensor layer, F5 (FR8) |
| 3 | No samples arriving at all | Communication layer, F14 or F16 (FR28) |
| 4 | Many joints on one stream anomalous at the same moment, with similar score | Add a stream-level common-cause hypothesis |
| 5 | Otherwise | Keep the joint or sensor hypothesis |

Rules 2 and 3 resolve the [tension between FR8 and FR28](../project/rasd-review.md#b1-fr8-and-fr28-can-be-read-as-contradictory): an invalid value inside a received sample is the sensor's fault, and an absent sample is the link's.

Rule 1 removes only hypotheses that are explained by missing data. A drifting joint on a lossy stream keeps its hypothesis, because its residual is still computed from the samples that did arrive. This is what S8 requires: "not explained away by the packet loss".

### Body regions

Regions are never diagnosed directly; their state derives from their members ([Diagnostic engine](diagnostic-engine.md#body-regions)).

## Stalls and missing hypotheses

A stalled classifier must not stop confirmations (S9). `DiagnosticEngine` therefore uses the latest `FaultLocalized` if it has one, and otherwise builds a provisional list from the evidence suggestions. `AlertManager` publishes `AlertUpdated` if better hypotheses arrive later.

## Testing

| Test | Verifies |
|---|---|
| F4 and F9 evidence gives both hypotheses above threshold, and the group is flagged | FR26, S3 |
| Hypotheses are sorted and come from the catalogue | FR25 |
| Every joint maps to its region; streams have none | FR27 |
| IMU stale with no joint hypothesis | FR28, S4 |
| NaN in received sample gives F5 on the sensor | FR8 |
| Drift + loss: both hypotheses survive | S8 |
| Rules-only produces hypotheses without a model | FR23 |

**Next:** [Diagnostic engine](diagnostic-engine.md)
