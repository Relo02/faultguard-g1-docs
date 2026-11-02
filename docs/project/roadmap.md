---
hide:
  - toc
---

# Roadmap

!!! baseline "Baseline"
    From the team's project plan (24 October 2026). Weeks count from the official start date, which the instructor has not yet confirmed.

The project runs 13 weeks. RASD, Design Document and implementation overlap, and the last week is buffer.

```mermaid
gantt
  title FaultGuard-G1: 13-week plan (dates are placeholders until the start date is confirmed)
  dateFormat YYYY-MM-DD
  axisFormat W%W
  section Setup
  Phase 0 Setup             :p0, 2027-01-04, 7d
  M0 Kickoff                :milestone, m0, 2027-01-10, 0d
  section Documents
  Phase 1 RASD              :p1, 2027-01-04, 28d
  Technical spikes          :sp, 2027-01-11, 21d
  M1 RASD v1.0              :milestone, m1, 2027-01-31, 0d
  Phase 2 Design Document   :p2, 2027-01-25, 28d
  M2 Design Document v1.0   :milestone, m2, 2027-02-21, 0d
  section Implementation
  Increment 1               :i1, 2027-02-01, 14d
  Increment 2               :i2, 2027-02-15, 14d
  Increment 3               :i3, 2027-02-22, 14d
  M3 End-to-end pipeline    :milestone, m3, 2027-03-07, 0d
  Increment 4               :i4, 2027-03-01, 14d
  Increment 5               :i5, 2027-03-08, 14d
  M4 Feature complete       :milestone, m4, 2027-03-21, 0d
  section Closing
  Phase 4 Verification      :v, 2027-03-01, 28d
  Phase 5 Finalization      :f, 2027-03-22, 14d
  M5 Documents aligned      :milestone, m5, 2027-03-28, 0d
  M6 Final submission       :milestone, m6, 2027-04-04, 0d
```

## Milestones

Each closes at the end of its week. **M3 is the critical one**, because everything after it builds on a working pipeline.

| Week | Milestone | Done when |
|---|---|---|
| W1 | M0 Kickoff | Repo created and instructor invited, LaTeX project set up, tech stack decided, roles agreed |
| W4 | M1 RASD v1.0 | All RASD sections, diagnostic FSM and sequence diagrams pushed to main, reviewed by all three |
| W7 | M2 Design Document v1.0 | Component, class and runtime views, patterns, traceability and test plan pushed to main |
| W9 | M3 End-to-end pipeline | Replayed data with an injected fault reaches CONFIRMED and raises an alert; automated tests pass |
| W11 | M4 Feature complete | Planned faults, rules + ML fusion, backpressure and operator UI working |
| W12 | M5 Documents aligned | RASD and Design Document updated to v1.1 to match the code; installation instructions written |
| W13 | M6 Final submission | Everything on main before the deadline; demo and presentation rehearsed |

**Follow the steps:** [Step-by-step playbook](playbook.md)
