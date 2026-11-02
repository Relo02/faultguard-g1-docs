# Evaluation metrics

!!! proposed "Proposed"
    The RASD leaves the exact definitions as `[TODO]`. FR57–FR60 are baseline; these definitions are proposed, to be agreed before running any campaign, so that the metrics are not tuned to the results.

## Matching a diagnosis to an injected fault

For an injected fault *f* with target *c*, onset *t<sub>on</sub>* and end *t<sub>off</sub>*, a `DiagnosticConfirmed` at time *t* on component *c′* **matches** *f* if:

- *t* ∈ [*t<sub>on</sub>*, *t<sub>off</sub>* + *G*], where the grace period *G* defaults to 3 s, and
- *c′* = *c* (joint-level match), or *c′* lies in the same region as *c* (region-level match only).

Each confirmed diagnosis matches at most one fault, chosen as the earliest eligible onset. Confirmations that occur before any onset, or that match no fault, count as false alarms. Monitoring-system diagnoses are scored separately, so that a run's own overload is not counted as a false alarm against joints.

## Metrics

| Metric | Definition | Unit |
|---|---|---|
| **Detection rate** | Faults with at least one joint-level or region-level match, divided by injected faults | [0, 1] |
| **False-alarm rate** | Unmatched confirmations, divided by replay time | Per hour; also reported per episode |
| **Detection delay** | *t* − *t<sub>on</sub>* for the first match, in source time | s: median, p90 |
| **Localization accuracy** | Among detected: joint-level matches / all matches; also region-level | [0, 1] |
| **Hypothesis accuracy** | Among detected: injected fault ranked first; and in the top 3 | [0, 1] |
| **Guided success** | Reports where the injected fault is within the top-k guided hypotheses (k = 3) | [0, 1] |

Delay and detection are reported **per fault class**, per **single vs combined**, and per **arm vs leg**, always side by side for hybrid and rules-only (FR58).

Nominal replay is a required part of every campaign, or the false-alarm rate has no denominator with fault-free conditions.

## Experimental design

```yaml
# campaigns/full.yaml
tasks: {split: test}             # held-out tasks only
episodes_per_task: 5
seeds: [1, 2, 3]
modes: [hybrid, rules_only]
scenarios:
  nominal: true
  single: [F1, F2, F3, F4, F5, F9, F10, F11, F12, F13, F14, F15, F16, F17, F18, F19]
  combined:
    - [F2, F14]       # S8
    - [F11, F15]
    - [F12, F2]       # same joint
targets: sampled per run, from joints applicable to each fault
```

Confidence intervals come from a bootstrap over episodes, since episodes from one task are correlated, and sessions from one episode more so. A seed alone doesn't produce independent data.

## Tentative targets

The RASD asks for target values. The project is judged mainly on architecture and the honesty of the evaluation, so these are placeholders until a first campaign runs. The hybrid mode beating rules-only is **not** assumed: if it doesn't, that is a result to report.

| Metric | Tentative target, Core faults, arms |
|---|---|
| Detection rate | ≥ 0.9 |
| False alarms | ≤ 1 per hour of nominal replay |
| Median detection delay | ≤ 3 s after the fault becomes detectable |
| Joint-level localization | ≥ 0.8 |
| Hypothesis top-3 | ≥ 0.8 |
| Guided success (k = 3) | ≥ 0.7 |

## Report contents

`report.json` holds every value with its confidence interval, plus configuration hash, model version and dataset revision. `summary.md` holds the tables for the Design Document and the final presentation. A run that lost data or has an untraceable alert is flagged in the report.

## Timing and load results

These are measured separately in real-time mode, not in the campaign: NFR1 (maximum confirmation latency), NFR2 (UI latency), NFR3 (queue occupancy at 1×, 2× and 5×), and NFR6 (memory over a long run, using chained episodes).
