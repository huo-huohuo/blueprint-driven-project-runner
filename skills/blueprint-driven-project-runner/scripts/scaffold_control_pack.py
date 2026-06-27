#!/usr/bin/env python3
"""Create a blueprint-control document pack for AI-assisted projects.

Examples:
  python scaffold_control_pack.py --project C:/repo
  python scaffold_control_pack.py --project . --module "Inventory" --module "Reporting"
  python scaffold_control_pack.py --project . --out docs/ai-control --dry-run
"""

from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_MODULES = [
    "Core Product",
    "Backend Platform",
    "Operations",
]


def slug(value: str) -> str:
    chars = [ch.lower() if ch.isalnum() else "-" for ch in value.strip()]
    result = "".join(chars)
    while "--" in result:
        result = result.replace("--", "-")
    return result.strip("-") or "module"


def prefix_for(module: str) -> str:
    return slug(module).upper().replace("-", "_")


def write_if_missing(path: Path, content: str, overwrite: bool, dry_run: bool) -> str:
    if path.exists() and not overwrite:
        return "exists"
    if dry_run:
        return "would-write"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return "written"


def record_template(
    record_id: str,
    record_type: str,
    title: str,
    target_behavior: list[str],
    preview: list[str],
    verification: str,
) -> str:
    target = "\n".join(f"- {line}" for line in target_behavior)
    preview_text = "\n".join(f"- {line}" for line in preview)
    return f"""### {record_id} {title}

ID: {record_id}
Type: {record_type}
Source:
- DECISION_NEEDED
Current Evidence:
- NOT_CHECKED
Target Behavior:
{target}
Forbidden Result:
- DECISION_NEEDED
Preview:
{preview_text}
Acceptance:
- DECISION_NEEDED
Verification:
- {verification}
Owner: DECISION_NEEDED
Status: draft
Confidence: low
Open Questions:
- DECISION_NEEDED
"""


def index_doc(modules: list[str], project_root: Path) -> str:
    rows = "\n".join(f"| {m} | | | | planned |" for m in modules)
    return f"""# AI Project Control Index

This project uses blueprint-bound AI execution. Broad implementation must cite executable blueprint records, execution ledger rows, allowed scope, forbidden scope, and acceptance evidence.

## Project Root

`{project_root}`

## Control Rule

No executable blueprint, no execution ledger, no long-running implementation. Summary briefs cannot authorize coding.

## Modules

| Module | Owner Thread | Scope | Forbidden Scope | Status |
| --- | --- | --- | --- | --- |
{rows}

## High-Conflict Areas

| Area | Current Owner | Rule |
| --- | --- | --- |
| app/router entrypoints | | serialize changes |
| shared database schema | | confirm before migration |
| access-control code | | owner only |
| background workers/cursors | | no cursor or offset mutation without approval |
| external side effects or production-like writes | | explicit human confirmation |

## Current Priority

| Date | Priority | Contract | Status |
| --- | --- | --- | --- |
| | | | |
"""


def run_card_doc() -> str:
    return """# Run Card

## Mode

Intake / Blueprint Compiler / Blueprint Audit / Ledger Compiler / Goal Prompt / Execution / Recovery / Coordination

## User Outcome

## Project Facts Read

-

## Discovery Brief

Short source-aware understanding. This section cannot authorize coding.

## Blocking Unknowns

-

## Next Artifact

Executable blueprint records / work slice / execution ledger / execution contract / evidence report / recovery plan
"""


def product_doc(module: str) -> str:
    prefix = prefix_for(module)
    record = record_template(
        f"{prefix}-PRODUCT-001",
        "product",
        "<workflow or surface>",
        ["DECISION_NEEDED"],
        [
            "workflow checklist: DECISION_NEEDED",
            "user journey: DECISION_NEEDED",
            "no-go list: DECISION_NEEDED",
        ],
        "DECISION_NEEDED",
    )
    return f"""# Product Blueprint: {module}

## Discovery Brief

Short context only. Do not use this section as an implementation contract.

## Users

| User | Daily Job | Pain | Success Signal |
| --- | --- | --- | --- |
| | | | |

## Scope

Owns:
-

Does not own:
-

## Executable Blueprint Records

{record}
"""


def interface_doc(module: str) -> str:
    prefix = prefix_for(module)
    record = record_template(
        f"{prefix}-INTERFACE-001",
        "interface",
        "<screen or state>",
        [
            "Initial state: DECISION_NEEDED",
            "Loading state: DECISION_NEEDED",
            "Empty state: DECISION_NEEDED",
            "Selected state: DECISION_NEEDED",
            "Error state: DECISION_NEEDED",
        ],
        [
            "target screenshot / wire preview / static preview / state checklist / DECISION_NEEDED",
        ],
        "browser screenshot / Playwright screenshot / manual screenshot / DECISION_NEEDED",
    )
    return f"""# Interface Blueprint: {module}

## Discovery Brief

Short context only. Do not use this section as an implementation contract.

## Executable Blueprint Records

{record}
## References

- screenshot/prototype:
- comparable product:
- notes:
"""


def engineering_doc(module: str) -> str:
    prefix = prefix_for(module)
    record = record_template(
        f"{prefix}-ENGINEERING-001",
        "engineering",
        "<service or data contract>",
        [
            "Business Scenario: DECISION_NEEDED",
            "Actor: DECISION_NEEDED",
            "Trigger: DECISION_NEEDED",
            "Before State: DECISION_NEEDED",
            "Action: DECISION_NEEDED",
            "After State: DECISION_NEEDED",
            "System Boundary: DECISION_NEEDED",
            "Data Contract: DECISION_NEEDED",
            "Operation Contract: DECISION_NEEDED",
            "Access Rule: DECISION_NEEDED",
            "Repeat/Idempotency Rule: DECISION_NEEDED",
            "Failure Behavior: DECISION_NEEDED",
            "Observability: DECISION_NEEDED",
        ],
        [
            "business flow checklist: DECISION_NEEDED",
            "before/after example: DECISION_NEEDED",
            "input/output sample: DECISION_NEEDED",
            "state rules: DECISION_NEEDED",
            "boundaries: DECISION_NEEDED",
            "failure matrix: DECISION_NEEDED",
            "evidence plan: DECISION_NEEDED",
        ],
        "unit test / API check / log check / DECISION_NEEDED",
    )
    return f"""# Engineering Blueprint: {module}

## Discovery Brief

Short context only. Do not use this section as an implementation contract.

## Executable Blueprint Records

{record}
## Data Write Policy

- Read-only:
- Local/cache writes:
- Production-like writes:
- Requires explicit confirmation:
"""


def acceptance_doc(module: str) -> str:
    prefix = prefix_for(module)
    record = record_template(
        f"{prefix}-ACCEPTANCE-001",
        "acceptance",
        "<golden case>",
        [
            "Given: DECISION_NEEDED",
            "When: DECISION_NEEDED",
            "Then: DECISION_NEEDED",
        ],
        [
            "golden case checklist: DECISION_NEEDED",
            "pass/fail table: DECISION_NEEDED",
        ],
        "unit/golden test / browser flow / API check / manual check / DECISION_NEEDED",
    )
    return f"""# Acceptance Blueprint: {module}

## Executable Blueprint Records

{record}
## Completion Criteria

-

## Stop Criteria

Stop and report if:
-
"""


def work_slices_doc(module: str) -> str:
    return f"""# Work Slices: {module}

| ID | Blueprint Records | Problem | Outcome | Appetite | Hill Position | Owner | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WS-001 | | | | | raw | | |

## Slice Detail: WS-001

Blueprint Records:
-
Problem:
User-visible Outcome:
Appetite:
Owned Files:
Forbidden Files:
Golden Cases:
No-gos:
Evidence:
"""


def maturity_doc(modules: list[str]) -> str:
    rows = "\n".join(f"| {m} | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | raw |" for m in modules)
    return f"""# Maturity Dashboard

| Module | Product Records | Interface Records | Engineering Records | Acceptance Records | Implementation | Real Data | Safety | Ops | Acceptance | Hill |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
{rows}

Scoring:
- 0: absent
- 25: drafted
- 50: structurally complete
- 75: ready or accepted with representative evidence
- 100: accepted with regression protection
"""


def ledger_doc() -> str:
    return """# Execution Ledger

This is the execution queue. Complete one row at a time, verify it, then update the row before moving on.

## Task Queue

| ID | Blueprint Records | Work Slice | Goal | Completion Path | Scope / Files | Acceptance Standard | Verification Method | Evidence | Status | Accepted? | Blocker / Skip Reason | Resume Condition | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LEDGER-001 | | | | | | | | | planned | no | | | |

Status values: planned / active / blocked / shelved / skipped / verified / accepted

## Run History

| Date | Contract ID | Ledger Rows | Files Changed | Evidence | Result | Next |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |
"""


def drift_doc() -> str:
    return """# Drift Log

Use this when AI work changes too much, loops without visible improvement, or violates an executable blueprint record.

| Date | Symptom | Root Cause | Files Involved | Prevention Rule | Status |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
"""


def decision_template_doc() -> str:
    return """# Decision Record: ADR-000 <title>

## Status

Proposed / Accepted / Superseded

## Context

What forces, constraints, or tradeoffs led to this decision?

## Decision

What will the project do?

## Consequences

Positive:
-

Negative:
-

Neutral:
-

## Supersedes / Superseded By

-
"""


def collect_outputs(root: Path, out_dir: Path, modules: list[str], overwrite: bool, dry_run: bool) -> list[tuple[Path, str]]:
    written: list[tuple[Path, str]] = []
    written.append((out_dir / "00-control-index.md", write_if_missing(out_dir / "00-control-index.md", index_doc(modules, root), overwrite, dry_run)))
    written.append((out_dir / "01-run-card.md", write_if_missing(out_dir / "01-run-card.md", run_card_doc(), overwrite, dry_run)))
    written.append((out_dir / "90-maturity-dashboard.md", write_if_missing(out_dir / "90-maturity-dashboard.md", maturity_doc(modules), overwrite, dry_run)))
    written.append((out_dir / "91-execution-ledger.md", write_if_missing(out_dir / "91-execution-ledger.md", ledger_doc(), overwrite, dry_run)))
    written.append((out_dir / "92-drift-log.md", write_if_missing(out_dir / "92-drift-log.md", drift_doc(), overwrite, dry_run)))
    written.append((out_dir / "decisions" / "ADR-000-template.md", write_if_missing(out_dir / "decisions" / "ADR-000-template.md", decision_template_doc(), overwrite, dry_run)))

    for module in modules:
        mod_dir = out_dir / slug(module)
        written.append((mod_dir / "product-blueprint.md", write_if_missing(mod_dir / "product-blueprint.md", product_doc(module), overwrite, dry_run)))
        written.append((mod_dir / "interface-blueprint.md", write_if_missing(mod_dir / "interface-blueprint.md", interface_doc(module), overwrite, dry_run)))
        written.append((mod_dir / "engineering-blueprint.md", write_if_missing(mod_dir / "engineering-blueprint.md", engineering_doc(module), overwrite, dry_run)))
        written.append((mod_dir / "acceptance-blueprint.md", write_if_missing(mod_dir / "acceptance-blueprint.md", acceptance_doc(module), overwrite, dry_run)))
        written.append((mod_dir / "work-slices.md", write_if_missing(mod_dir / "work-slices.md", work_slices_doc(module), overwrite, dry_run)))

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an AI project control pack.")
    parser.add_argument("--project", required=True, help="Project root")
    parser.add_argument("--module", action="append", dest="modules", help="Module name; may repeat")
    parser.add_argument("--out", default="docs/ai-control", help="Output directory relative to project root")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    parser.add_argument("--dry-run", action="store_true", help="Print planned writes without changing files")
    args = parser.parse_args()

    root = Path(args.project).resolve()
    modules = args.modules or DEFAULT_MODULES
    out_dir = root / args.out

    for path, status in collect_outputs(root, out_dir, modules, args.overwrite, args.dry_run):
        print(f"{status}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
