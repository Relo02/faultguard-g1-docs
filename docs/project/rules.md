# Working rules

!!! baseline "Baseline"
    From the project plan.

One weekly check-in and one repository keep the three members aligned with the plan.

- **Weekly sync** (1 hour, day to agree): progress against the plan, blockers, tasks for the next week.
- **One repo for everything:** documents and code live in the project repo; `main` holds only reviewed work.
- **Branches and reviews:** each task on its own branch, merged through a pull request reviewed by another member.
- **Traceable IDs:** every goal, requirement and assumption gets an ID, reused in the Design Document traceability tables and in test names.
- **Versioned documents:** drafts are v0.x, the first release is v1.0, and each change is logged in the revision history.
- **Shared context:** after each milestone, update the project context files so nobody works from stale information.

## Keeping this site current

Add one rule: when a decision on this site changes, update the page in the same week, and change its label from *Proposed* to *Baseline* once it enters the Design Document. A public site that drifts from the deliverables is worse than none.
