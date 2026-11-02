# Objectives

!!! baseline "Baseline"
    From the project proposal v2.0 and RASD v0.1 §1.1.

## The problem

A humanoid such as the Unitree G1 combines dozens of actuated joints, inertial and tactile sensors, and a communication stack that streams telemetry at tens of hertz. A fault in any of these can degrade a task long before a human notices: a drifting encoder, a joint that stops following its command, a link that drops packets. A wrong alert can cost almost as much as a missed one.

Fault detection and diagnosis is an established discipline. Doing it in real time on imperfect telemetry, and keeping the system open to new faults, is above all a **software engineering problem**. That is what this project is about.

## What the project is, and is not

| It is | It is not |
|---|---|
| An architecture for a diagnostic system that is dependable and extensible | A search for the single best fault classifier |
| A pipeline with separate detection, classification, localization and decision stages | One model that goes straight from telemetry to an alert |
| A system that keeps working, and says what it lost, when telemetry degrades | A system that assumes clean, synchronized data |
| Observation only | Recovery, actuation or control of the robot |

## Project objectives and how each is proven

| Objective | How it is validated |
|---|---|
| **Extensibility** (primary) | A new fault type is one new injector class plus one configuration entry. A new check is one new rule or strategy. No existing component changes, shown by the commit diff and a live demo. |
| **Timeliness** | When the evidence reaches the confirmation threshold, `DiagnosticConfirmed` is published within 2 s of the last contributing sample, at 1× replay. |
| **Robustness under load** | Up to 5× replay, every queue stays within its bound, the declared overload policy applies, and dropped data is reported as a monitoring-system fault. |
| **Diagnostic stability** | Under evidence fluctuating near a threshold, the state machine does not oscillate faster than the dwell time allows. |
| **Diagnostic quality** | Detection rate, false-alarm rate, detection delay and localization accuracy for each fault class, against a rules-only baseline. |
| **Guided diagnosis** (secondary) | For scripted symptom reports, the injected fault ranks among the orchestrator's top hypotheses; the success rate is reported. |

!!! note "What cannot be cut"
    The event-driven core, the diagnostic state machine, rules + ML fusion, backpressure and the extensibility demo are the instructor's conditions for approval. See [risks and cut order](../project/risks.md).

## Goals

Goals are stated in terms of the world: the robot, its operator, and the people who validate and maintain the system.

| ID | Goal |
|---|---|
| G1 | Faults of the robot's sensors and joints, of its telemetry communication, and of the monitoring system itself are detected, classified and localized, and the operator is informed of them in a timely manner. |
| G2 | The operator receives only diagnoses backed by sufficient evidence over time, and the reported state of a component does not oscillate when the evidence is borderline. |
| G3 | Diagnosis keeps working when telemetry is asynchronous, delayed, lost, out of order or arrives faster than it can be processed, and any loss of diagnostic coverage is made visible to the operator. |
| G4 | New fault types and new diagnostic checks can be added without modifying the components that already exist. |
| G5 | Every diagnostic conclusion can be traced back to the evidence and the telemetry that produced it. |
| G6 | The diagnostic quality of the system can be measured objectively against known faults and compared with a rules-only baseline. |
| G7 | (Secondary.) An operator who notices a symptom can describe it in natural language and obtain a ranked list of plausible faults, together with the tests that support them. |

## Who it serves

| User | Needs | Interacts through |
|---|---|---|
| **Operator** supervises the robot during a task; knows the robot, not necessarily signal processing or ML | A clear, stable view of what is healthy, alerts they can trust, a way to see *why*, a quick way to ask about a symptom | User interface only |
| **Test engineer** validates the system | Fault scenarios, sessions and batch campaigns at various replay rates, event logs, evaluation reports | Configuration files, CLI, reports |
| **Developer** maintains and extends the system | To add faults, injectors, rules, detectors, skills or sources without changing existing components | Code and configuration |

Two external systems also interact with it: the **telemetry source**, which only provides data, and the **LLM/VLM service**, whose answers are treated as untrusted.

**Next:** [System at a glance](system.md)
