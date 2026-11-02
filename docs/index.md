---
title: FaultGuard-G1
hide:
  - navigation
---

# FaultGuard-G1

**A dependable, extensible, real-time diagnostic system for a humanoid robot.**

FaultGuard-G1 watches the telemetry of a Unitree G1 and works out what is wrong with the robot: which sensor, joint, communication stream or part of the monitoring system itself has a fault, how sure it is, and why. It only observes. It never commands the robot.

The focus of the project is the *software architecture*, not the best possible classifier. Detection, classification, localization and decision are separate stages. Deterministic rules and machine-learning detectors contribute evidence side by side. The set of diagnosable faults can grow without changing the components that already exist.

This site is the technical reference the team builds from. Read it from top to bottom to go from objectives to the code-level design, or jump to the part you need.

<div class="grid cards" markdown>

-   :material-bullseye-arrow: **1. Overview**

    ---

    Why the system exists, what it does, where its boundary lies and what data it runs on.

    [Objectives](overview/objectives.md) · [At a glance](overview/system.md) · [Telemetry data](overview/dataset.md)

-   :material-clipboard-text-outline: **2. Requirements**

    ---

    Scenarios, domain model, the 19 fault types, 60 functional and 20 non-functional requirements, state machines.

    [Start here](requirements/index.md)

-   :material-sitemap-outline: **3. Architecture**

    ---

    Components, events, runtime behaviour, concurrency, patterns and technology.

    [Start here](architecture/index.md)

-   :material-code-braces: **4. Low-level design**

    ---

    Packages, types, algorithms and configuration for each component, ready to implement.

    [Start here](design/index.md)

-   :material-check-decagram-outline: **5. Verification**

    ---

    Test strategy, exact metric definitions, and a trace from every requirement to its design element and test.

    [Test strategy](verification/strategy.md) · [Traceability](verification/traceability.md)

-   :material-timeline-check-outline: **6. Project execution**

    ---

    The 13-week plan turned into steps, with what to read, what to produce and when each step is done.

    [Playbook](project/playbook.md) · [Open decisions](project/decisions.md)

</div>

!!! tip "Diagrams"
    Click any diagram to enlarge it, and click again to close it.

## How far to trust each page

Every technical page says where its content comes from:

!!! baseline "Baseline"
    Taken from the project proposal v2.0 or RASD v0.1. If this site and the RASD disagree, the RASD wins.

!!! proposed "Proposed"
    A design this documentation puts forward to make implementation possible. It has **not** been agreed by the team yet, and it enters the Design Document only after review. The major choices are listed in the [decision records](reference/adrs.md).

## Read this first

Checking RASD v0.1 against the real dataset and against itself produced findings that change the plan. The three most important are:

!!! warning "Three issues to settle before the RASD reaches v1.0"
    1. **The G1 recordings hold no leg commands.** Tracking-error checks work only on arms and hands, yet scenario S2 uses one on the left knee.
    2. **Episodes average about 14.6 s.** Scenario S2 starts its fault at 20 s, after most episodes have ended, so replay must be able to chain episodes.
    3. **The state machine does not fully guarantee NFR7.** Nothing stops a component going HEALTHY → SUSPECTED immediately after SUSPECTED → HEALTHY.

    See the [full list of findings](project/rasd-review.md).

## Project at a glance

| Item | Detail |
|---|---|
| **Course** | Software Engineering for Automation, Politecnico di Milano, A.Y. 2026–2027 |
| **Instructor** | Prof. Matteo Camilli |
| **Team** | Lorenzo Ortolani, Olgun Bulun, Mateo Gomez Abril |
| **Duration** | 13 weeks from the official start date (W1–W13) |
| **Deliverables** | D1 RASD, D2 Design Document, D3 Implementation |
| **Requirements baseline** | RASD v0.1, 24 October 2026 |
