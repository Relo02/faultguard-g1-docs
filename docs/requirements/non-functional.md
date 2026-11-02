# Non-functional requirements

!!! baseline "Baseline"
    From RASD v0.1 §2.5. Each is stated so that it can be verified. *Open* marks a `[TODO]` from the RASD; see [Open decisions](../project/decisions.md).

## Performance and timeliness

| ID | Requirement | Verification | Goals |
|---|---|---|---|
| NFR1 | When the evidence for a fault reaches the confirmation condition, the system shall publish the diagnostic confirmation within 2 s of the receive time of the last contributing sample, at 1× replay rate. | Timestamps in the event log, over all scenarios of a campaign; maximum reported. | G1 |
| NFR2 | The user interface shall show a state change or an alert within 1 s of its publication. *Open: confirm value.* | Instrumented timestamps in the user interface. | G1 |

## Robustness

| ID | Requirement | Verification | Goals |
|---|---|---|---|
| NFR3 | At replay rates up to 5×, every internal queue shall stay within its configured bound, the declared overload policy shall be applied, and the discarded data shall be reported as a monitoring-system fault. | Load tests at 1×, 2× and 5× with logging of queue occupancy. | G3 |
| NFR4 | Delayed, lost, reordered, missing or non-numeric telemetry shall never cause the system to stop or crash. | Injection test suite covering F5 and F13–F16. | G3 |
| NFR5 | The failure of a single check or pipeline component shall not stop the other components, and shall be reported as a monitoring-system fault. | Tests with a deliberately failing check and with stall injection (F18). | G3 |
| NFR6 | Memory use shall remain bounded during a continuous session of at least *(Open: 60)* minutes at 5× replay rate. | Memory profiling of a long run. | G3 |

## Diagnostic stability and quality

| ID | Requirement | Verification | Goals |
|---|---|---|---|
| NFR7 | Under evidence that fluctuates near a threshold, two consecutive transitions between HEALTHY and SUSPECTED of the same component shall be at least T<sub>dwell</sub> apart. | Scripted borderline scenarios (S6); transitions counted in the event log. | G2 |
| NFR8 | For every implemented fault class, single and combined, detection rate, false-alarm rate, detection delay and localization accuracy shall be measured and reported against the rules-only baseline. *Open: set target values.* | Evaluation campaign (S11). | G6, G1 |
| NFR9 | For the scripted symptom reports, the success rate of guided diagnosis (injected fault among the top-k hypotheses) shall be measured and reported. *Open: fix k and a target.* | Evaluation campaign. | G7 |

## Extensibility and maintainability

Extensibility is the primary objective of the project.

| ID | Requirement | Verification | Goals |
|---|---|---|---|
| NFR10 | A new fault type shall be addable as one new injector class and one configuration entry, with no change to existing components. | Commit diff and live demo. | G4 |
| NFR11 | A new diagnostic check shall be addable as one new rule or detector class and one configuration entry, with no change to existing components. | Commit diff and live demo. | G4 |
| NFR12 | A new diagnostic skill shall be addable as one new class registered in the skill registry, with no change to existing components. | Commit diff. | G4, G7 |
| NFR13 | A new telemetry source shall be addable as one new adapter, with no change to the diagnostic components. | Commit diff. | G4 |

## Traceability and testability

| ID | Requirement | Verification | Goals |
|---|---|---|---|
| NFR14 | Every alert shall be traceable, through correlation IDs, to all the evidence and telemetry samples that contributed to it. | Automated check of the event log of a campaign: 100% of alerts traceable. | G5 |
| NFR15 | Given the same episode, fault scenario, seed, configuration and the rule-based planner, two runs shall produce the same set of confirmed diagnoses. *Open: must order and timing also match?* | Repeated runs compared automatically. | G6 |
| NFR16 | The LLM/VLM service shall be replaceable by a stub in automated tests. | Test suite runs without network access. | G6, G7 |

## Safety, usability and portability

| ID | Requirement | Verification | Goals |
|---|---|---|---|
| NFR17 | The system shall never send commands to the robot; its access to telemetry sources shall be read-only. | Inspection of the source interface and of the skill interface. | Scope |
| NFR18 | From the main view, the operator shall reach the evidence of an alert, and acknowledge the alert, in at most *(Open: two)* interactions each. | Walkthrough of the user interface. | G1, G5 |
| NFR19 | Diagnostic states shall be shown with both a colour and a text label, consistently across views. | Inspection of the user interface. | G1 |
| NFR20 | The Diagnostic System and the Validation Harness shall run on a standard laptop *(Open: state OS, CPU and RAM)* without a GPU; the LLM/VLM service may be remote. | Installation on the team's machines. | Scope |
