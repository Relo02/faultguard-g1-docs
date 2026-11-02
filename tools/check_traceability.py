#!/usr/bin/env python3
"""Check that requirement IDs are complete and traced. Standard library only.

Fails (exit 1) if:
  - FR1..FR60 or NFR1..NFR20 are not all defined on the requirement pages;
  - a requirement is missing from docs/verification/traceability.md, or that page
    names an ID that does not exist.

Reports, without failing, entries of a requirement's Goals column that are absent
from the goal map (RASD Table 2.17). Those gaps are a known finding in the RASD
and the map reproduces it on purpose, so they must not break the build.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
ROW = re.compile(r"^\|\s*(N?FR\d+)\s*\|(.*)\|\s*$", re.M)
GOAL_ROW = re.compile(r"^\|\s*(G\d)\s*\|([^|]*)\|", re.M)
ID = re.compile(r"\bN?FR\d+\b")
GOAL = re.compile(r"\bG\d\b")


def defined(path: Path) -> dict[str, set[str]]:
    """Requirement ID -> goals named in the last column of its row."""
    rows = {}
    for req, rest in ROW.findall(path.read_text()):
        rows[req] = set(GOAL.findall(rest.split("|")[-1]))
    return rows


def main() -> int:
    req = DOCS / "requirements"
    fr, nfr = defined(req / "functional.md"), defined(req / "non-functional.md")
    errors = []

    expected = {f"FR{i}" for i in range(1, 61)} | {f"NFR{i}" for i in range(1, 21)}
    all_defined = fr | nfr
    if missing := expected - set(all_defined):
        errors.append(f"not defined on the requirement pages: {sorted(missing)}")
    if extra := set(all_defined) - expected:
        errors.append(f"unexpected IDs on the requirement pages: {sorted(extra)}")

    traced = dict(ROW.findall((DOCS / "verification" / "traceability.md").read_text()))
    if missing := expected - set(traced):
        errors.append(f"missing from traceability.md: {sorted(missing)}")
    if extra := set(traced) - expected:
        errors.append(f"unknown IDs in traceability.md: {sorted(extra)}")
    for rid, rest in traced.items():
        if not rest.split("|")[0].strip():
            errors.append(f"{rid} has no design element in traceability.md")

    goal_map = {g: set(ID.findall(ids)) for g, ids in GOAL_ROW.findall((req / "index.md").read_text())}
    for goal in sorted(goal_map):
        gaps = sorted((r for r, gs in all_defined.items() if goal in gs and r not in goal_map[goal]),
                      key=lambda r: (r.startswith("N"), int(re.sub(r"\D", "", r))))
        if gaps:
            print(f"note: {goal} is in the Goals column of {', '.join(gaps)}, but not in the goal map")
        reverse = sorted(goal_map[goal] - {r for r, gs in all_defined.items() if goal in gs})
        if reverse:
            print(f"note: the goal map lists {', '.join(reverse)} under {goal}, but their Goals column does not")

    for err in errors:
        print(f"ERROR: {err}", file=sys.stderr)
    print(f"checked {len(all_defined)} requirements: {'FAILED' if errors else 'all traced'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
