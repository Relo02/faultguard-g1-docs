# Deliverables

!!! baseline "Baseline"
    From the course project guideline and the team's deliverables overview.

Deliverables are reviewed together at a final discussion. The evaluation assesses the quality of the artifacts (precision, conceptual and technical soundness, completeness, consistency) and the quality of the presentation, including fitting the allowed time.

| | Answers | Contains |
|---|---|---|
| **D1 RASD** | What must the system do? | Scenarios, domain model, requirements, supporting models |
| **D2 Design Document** | How is it built? | Components, classes, sequence diagrams, patterns, UI, traceability, test plan |
| **D3 Implementation** | Does it run? | Code consistent with D1 and D2, installation instructions. A stable prototype matters more than many features. |

## Rules that apply to all of them

- Groups of 2 or 3. The artifacts are due within **3 months of the agreed start date**. A delay notified in advance is tolerated but may carry a penalty.
- Artifacts are released by pushing to the `main` branch of a **private** GitHub repository named after the group members, with write access for all members and the instructor (`matteocamilli`) invited.
- There is one directory per deliverable.
- Material is not fixed in stone: updates are encouraged at any point before the final submission.
- D1 and D2 each need a **front page** (title, version, names, release date) and a **table of contents** with the first three heading levels and page numbers.

!!! warning "This documentation site is public"
    The guideline asks for the project repository to be private, and this site is deliberately separate from it. It publishes the requirements and proposed design. Before relying on it for the course, confirm with the instructor that a public companion site is acceptable, and keep the official artifacts in the private repository.

## D1: RASD structure

1. **Introduction**: purpose (goals), scope (world and shared phenomena), definitions, document structure.
2. **Overall description**: scenarios, domain model, user characteristics, product functions, nonfunctional aspects, assumptions, dependencies and constraints.
3. **Additional models**: requirements-level sequence diagrams, finite state machines.
4. **References.**

v0.1 of this document already exists; see [Requirements](../requirements/index.md) and the [findings to address](../project/rasd-review.md).

## D2: Design Document structure

| Guideline chapter | Where the input is on this site |
|---|---|
| 1 Introduction: purpose, definitions, revision history, structure | [Objectives](objectives.md), [Glossary](../reference/glossary.md) |
| 2A Component view: component diagram, components, main operations of the interfaces | [Component view](../architecture/components.md), [Event catalogue](../architecture/events.md) |
| 2B Class view | [Low-level design](../design/index.md) |
| 2C Runtime view: sequence diagrams per scenario | [Runtime view](../architecture/runtime.md) |
| 2D Styles and patterns: which, why and how | [Styles and patterns](../architecture/patterns.md), [Concurrency](../architecture/concurrency.md) |
| 3 User interface design | [Operator UI](../design/ui.md) |
| 4 Requirements traceability | [Traceability](../verification/traceability.md) |
| 5 Implementation, integration and test plan | [Playbook](../project/playbook.md), [Test strategy](../verification/strategy.md) |
| References | [References](../reference/references.md) |

The guideline numbers the references chapter 7 although there is no chapter 6; the team agreed to use chapter 6.

## D3: Implementation

Must include the code ready to install and run, and installation instructions covering prerequisites, dependencies and assumptions. No language or framework is imposed. A viable prototype is expected rather than a market-ready product, and nice-to-have features can be left out in favour of stability and code quality.

**Next section:** [Requirements](../requirements/index.md)
