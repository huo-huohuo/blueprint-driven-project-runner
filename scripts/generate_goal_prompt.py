#!/usr/bin/env python3
"""Generate a goal-mode prompt from ready executable blueprint records.

Examples:
  python generate_goal_prompt.py --project C:/repo --module "Inventory" --record INVENTORY-IMPORT-001 --work-slice WS-INVENTORY-001 --ledger-row LEDGER-INVENTORY-001
  python generate_goal_prompt.py --project . --module "Reporting" --record REPORTING-UI-001 --work-slice WS-REPORTING-001 --ledger-row LEDGER-REPORTING-001 --out docs/ai-control/reporting/goal-prompts/reporting-ui.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FIELD_NAMES = [
    "ID",
    "Type",
    "Source",
    "Current Evidence",
    "Target Behavior",
    "Forbidden Result",
    "Preview",
    "Acceptance",
    "Verification",
    "Owner",
    "Status",
    "Confidence",
    "Open Questions",
]

READY_STATUSES = {"ready", "accepted"}
FIELD_RE = re.compile(
    r"^(ID|Type|Source|Current Evidence|Target Behavior|Forbidden Result|Preview|Acceptance|Verification|Owner|Status|Confidence|Open Questions):\s*(.*)$"
)


def slug(value: str) -> str:
    chars = [ch.lower() if ch.isalnum() else "-" for ch in value.strip()]
    result = "".join(chars)
    while "--" in result:
        result = result.replace("--", "-")
    return result.strip("-") or "module"


def compact(lines: list[str]) -> str:
    return " ".join(line.strip() for line in lines if line.strip()).strip()


def bullet_block(lines: list[str], indent: str = "- ") -> str:
    cleaned = [line.strip() for line in lines if line.strip()]
    if not cleaned:
        return f"{indent}DECISION_NEEDED"
    output: list[str] = []
    for line in cleaned:
        if line.startswith("- "):
            output.append(line)
        else:
            output.append(f"{indent}{line}")
    return "\n".join(output)


def parse_records(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    records: list[dict[str, object]] = []
    current: dict[str, list[str]] | None = None
    current_field: str | None = None

    for raw in text.splitlines():
        line = raw.strip().lstrip("\ufeff")
        match = FIELD_RE.match(line)
        if match:
            field = match.group(1)
            value = match.group(2).strip()
            if field == "ID":
                if current:
                    current["_path"] = [str(path)]
                    records.append(current)  # type: ignore[arg-type]
                current = {}
            if current is None:
                current = {}
            current[field] = [value] if value else []
            current_field = field
            continue
        if current is not None and current_field and line:
            current[current_field].append(line)

    if current:
        current["_path"] = [str(path)]
        records.append(current)  # type: ignore[arg-type]
    return records


def find_blueprint_files(root: Path, module: str | None) -> list[Path]:
    base = root / "docs" / "ai-control"
    if module:
        module_dir = base / slug(module)
        if module_dir.exists():
            return sorted(path for path in module_dir.rglob("*blueprint*.md") if path.is_file())
    return sorted(path for path in base.rglob("*blueprint*.md") if path.is_file())


def load_records(root: Path, module: str | None) -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for path in find_blueprint_files(root, module):
        for record in parse_records(path):
            record_id = compact(record.get("ID", []))  # type: ignore[arg-type]
            if record_id:
                records[record_id] = record
    return records


def ensure_ready(record: dict[str, object], record_id: str) -> None:
    missing = [field for field in FIELD_NAMES if field not in record]
    if missing:
        raise ValueError(f"{record_id}: missing fields: {', '.join(missing)}")
    combined = "\n".join(compact(record.get(field, [])) for field in FIELD_NAMES)  # type: ignore[arg-type]
    if "DECISION_NEEDED" in combined:
        raise ValueError(f"{record_id}: contains DECISION_NEEDED")
    status = compact(record.get("Status", [])).lower()  # type: ignore[arg-type]
    if status not in READY_STATUSES:
        raise ValueError(f"{record_id}: status is {status!r}, not ready/accepted")


def render_prompt(
    root: Path,
    module: str,
    records: list[dict[str, object]],
    work_slice: str,
    ledger_rows: list[str],
) -> str:
    record_sections: list[str] = []
    verification_lines: list[str] = []
    forbidden_lines: list[str] = []
    for record in records:
        record_id = compact(record.get("ID", []))  # type: ignore[arg-type]
        record_sections.append(
            f"""### {record_id}

Type: {compact(record.get("Type", []))}
Source:
{bullet_block(record.get("Source", []))}
Target Behavior:
{bullet_block(record.get("Target Behavior", []))}
Preview:
{bullet_block(record.get("Preview", []))}
Acceptance:
{bullet_block(record.get("Acceptance", []))}
"""
        )
        verification_lines.append(f"- {record_id}: {compact(record.get('Verification', []))}")  # type: ignore[arg-type]
        forbidden_lines.append(f"- {record_id}: {compact(record.get('Forbidden Result', []))}")  # type: ignore[arg-type]

    record_ids = ", ".join(compact(record.get("ID", [])) for record in records)  # type: ignore[arg-type]
    ledger_row_lines = "\n".join(f"- {row}" for row in ledger_rows)

    return f"""# Goal Prompt: {module}

Use $blueprint-driven-project-runner.

## Project

Project root: {root}
Module: {module}
Mode: Execution

## Target Mode Startup Gate

Gate result: must be PASS before implementation.

PASS only if:
- project operating standard or equivalent repo rules have been read
- referenced blueprint records are ready or accepted: {record_ids}
- work slice is bounded: {work_slice}
- execution ledger file and row IDs are present: docs/ai-control/91-execution-ledger.md / {", ".join(ledger_rows)}
- this goal prompt passes lint or manual lint is documented
- execution contract states allowed scope, forbidden scope, data policy, verification, evidence, and stop condition

If the gate is FAIL, do not edit product code. Switch to Blueprint Compiler, Blueprint Audit, Ledger Compiler, Goal Prompt, Status, or Recovery mode.

## First Principle

Complete the referenced executable blueprint records and execution ledger rows exactly, with evidence. Do not optimize beyond the records, invent adjacent work, or rewrite unrelated areas.

## Read First

- AGENTS.md
- docs/ai-control/00-operating-standard.md
- docs/ai-control/00-control-index.md
- relevant module blueprint files
- relevant work-slices.md
- docs/ai-control/91-execution-ledger.md
- current git status

## Blueprint Records

{chr(10).join(record_sections)}

## Work Slice

ID: {work_slice}
Blueprint Records: {record_ids}
Outcome: implement and verify only the referenced records.
Appetite: bounded to the referenced records and their verification plan.

## Execution Ledger

Ledger file: docs/ai-control/91-execution-ledger.md
Rows:
{ledger_row_lines}

Work one ledger row at a time. Mark a row verified only after evidence passes. Mark it blocked or shelved with a reason and resume condition if it cannot be completed, then continue to the next independent row.

## Allowed Changes

- Only files required to complete the referenced blueprint records.
- Update tests, golden cases, docs/ai-control ledgers, and evidence artifacts when needed.

## Forbidden Changes

{chr(10).join(forbidden_lines)}
- Do not change unrelated modules.
- Do not perform high-risk actions without explicit user confirmation.
- Do not expand scope because a better adjacent idea appears.

## Data Policy

- Follow docs/ai-control/00-operating-standard.md.
- Treat production-like writes, destructive changes, external side effects, deployment, access-control, and migration changes as high risk.

## Verification Plan

{chr(10).join(verification_lines)}
- Run the strongest feasible verification and report any skipped checks.

## Evidence Required In Final Response

- blueprint record ids addressed
- files changed
- verification results
- preview/actual comparison when relevant
- golden case pass/fail when relevant
- risks
- rollback path

## Stop Conditions

Stop when:
- referenced blueprint records and ledger rows are implemented and verified or explicitly shelved/skipped with reasons
- a required change exceeds allowed scope
- blueprint contradiction is found
- verification cannot run
- high-risk action needs confirmation and cannot be shelved while independent rows remain
- unrelated worktree changes may be overwritten

## Unexpected Discoveries

Record as backlog, drift log, or open question. Do not implement outside the referenced records.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a goal-mode prompt from ready blueprint records.")
    parser.add_argument("--project", required=True, help="Project root")
    parser.add_argument("--module", required=True, help="Module name")
    parser.add_argument("--record", action="append", dest="records", required=True, help="Blueprint record ID; may repeat")
    parser.add_argument("--work-slice", required=True, help="Bounded work slice ID")
    parser.add_argument("--ledger-row", action="append", dest="ledger_rows", required=True, help="Execution ledger row ID; may repeat")
    parser.add_argument("--out", help="Write prompt to this file instead of stdout")
    args = parser.parse_args()

    root = Path(args.project).resolve()
    all_records = load_records(root, args.module)
    selected: list[dict[str, object]] = []

    for record_id in args.records:
        if record_id not in all_records:
            raise SystemExit(f"ERROR: record not found: {record_id}")
        record = all_records[record_id]
        try:
            ensure_ready(record, record_id)
        except ValueError as exc:
            raise SystemExit(f"ERROR: {exc}") from exc
        selected.append(record)

    prompt = render_prompt(root, args.module, selected, args.work_slice, args.ledger_rows)

    if args.out:
        out = Path(args.out).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(prompt, encoding="utf-8", newline="\n")
        print(f"written: {out}")
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
