#!/usr/bin/env python3
"""Generate a thread handoff package from ready blueprint records.

Examples:
  python generate_handoff_package.py --project C:/repo --module "Inventory" --record INVENTORY-IMPORT-001 --work-slice WS-IMPORT-001
  python generate_handoff_package.py --project . --module "Reporting" --record REPORTING-UI-001 --work-slice WS-UI-001 --out docs/ai-control/reporting/handoffs/ui-pass
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

from generate_goal_prompt import compact, ensure_ready, load_records, render_prompt, slug


def bullet_block(lines: list[str]) -> str:
    cleaned = [line.strip() for line in lines if line.strip()]
    if not cleaned:
        return "- DECISION_NEEDED"
    return "\n".join(line if line.startswith("- ") else f"- {line}" for line in cleaned)


def render_records(records: list[dict[str, object]]) -> str:
    chunks: list[str] = ["# Blueprint Records", ""]
    for record in records:
        record_id = compact(record.get("ID", []))  # type: ignore[arg-type]
        chunks.extend([
            f"## {record_id}",
            "",
            f"Type: {compact(record.get('Type', []))}",
            f"Status: {compact(record.get('Status', []))}",
            f"Owner: {compact(record.get('Owner', []))}",
            "",
            "Source:",
            bullet_block(record.get("Source", [])),  # type: ignore[arg-type]
            "",
            "Target Behavior:",
            bullet_block(record.get("Target Behavior", [])),  # type: ignore[arg-type]
            "",
            "Forbidden Result:",
            bullet_block(record.get("Forbidden Result", [])),  # type: ignore[arg-type]
            "",
            "Preview:",
            bullet_block(record.get("Preview", [])),  # type: ignore[arg-type]
            "",
            "Acceptance:",
            bullet_block(record.get("Acceptance", [])),  # type: ignore[arg-type]
            "",
            "Verification:",
            bullet_block(record.get("Verification", [])),  # type: ignore[arg-type]
            "",
        ])
    return "\n".join(chunks)


def render_activation(root: Path, module: str, out_dir: Path) -> str:
    return f"""# Activation Prompt

Use $blueprint-driven-project-runner.

Project root: {root}
Module: {module}
Mode: Execution

Do not rely on chat history. Read this handoff package first:

- {out_dir / "handoff-summary.md"}
- {out_dir / "goal-prompt.md"}
- {out_dir / "blueprint-records.md"}
- {out_dir / "verification-plan.md"}

Then read the project governance files:

- AGENTS.md
- docs/ai-control/00-operating-standard.md
- docs/ai-control/00-control-index.md

Follow the goal prompt exactly. The first principle is to complete the referenced executable blueprint records with evidence, without expanding scope.
"""


def render_summary(root: Path, module: str, records: list[dict[str, object]], work_slice: str, out_dir: Path) -> str:
    ids = [compact(record.get("ID", [])) for record in records]  # type: ignore[arg-type]
    return f"""# Handoff Summary

Project root: `{root}`
Module: `{module}`
Work slice: `{work_slice}`
Package path: `{out_dir}`

## Blueprint Records

{chr(10).join(f"- {record_id}" for record_id in ids)}

## Scope Rule

Complete only the referenced records. Do not change unrelated modules, expand scope, or implement adjacent ideas.

## Completion Report Must Include

- blueprint record ids addressed
- files changed
- verification results
- preview/actual comparison when relevant
- golden case pass/fail when relevant
- risks
- rollback path
"""


def render_verification(records: list[dict[str, object]]) -> str:
    lines = ["# Verification Plan", ""]
    for record in records:
        record_id = compact(record.get("ID", []))  # type: ignore[arg-type]
        lines.extend([
            f"## {record_id}",
            "",
            "Verification:",
            bullet_block(record.get("Verification", [])),  # type: ignore[arg-type]
            "",
            "Acceptance:",
            bullet_block(record.get("Acceptance", [])),  # type: ignore[arg-type]
            "",
        ])
    return "\n".join(lines)


def write(path: Path, content: str, dry_run: bool) -> str:
    if dry_run:
        return "would-write"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return "written"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a thread handoff package from ready blueprint records.")
    parser.add_argument("--project", required=True, help="Project root")
    parser.add_argument("--module", required=True, help="Module name")
    parser.add_argument("--record", action="append", dest="records", required=True, help="Blueprint record ID; may repeat")
    parser.add_argument("--work-slice", required=True, help="Work slice ID")
    parser.add_argument("--out", help="Output directory; defaults to docs/ai-control/<module>/handoffs/<timestamp>")
    parser.add_argument("--dry-run", action="store_true", help="Print planned writes without changing files")
    args = parser.parse_args()

    root = Path(args.project).resolve()
    all_records = load_records(root, args.module)
    selected: list[dict[str, object]] = []
    for record_id in args.records:
        record = all_records.get(record_id)
        if not record:
            raise SystemExit(f"ERROR: record not found: {record_id}")
        try:
            ensure_ready(record, record_id)
        except ValueError as exc:
            raise SystemExit(f"ERROR: {exc}") from exc
        selected.append(record)

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.out).resolve() if args.out else root / "docs" / "ai-control" / slug(args.module) / "handoffs" / f"{slug(args.work_slice)}-{timestamp}"
    goal_prompt = render_prompt(root, args.module, selected, args.work_slice)

    files = [
        (out_dir / "activation-prompt.md", render_activation(root, args.module, out_dir)),
        (out_dir / "handoff-summary.md", render_summary(root, args.module, selected, args.work_slice, out_dir)),
        (out_dir / "goal-prompt.md", goal_prompt),
        (out_dir / "blueprint-records.md", render_records(selected)),
        (out_dir / "verification-plan.md", render_verification(selected)),
    ]

    for path, content in files:
        print(f"{write(path, content, args.dry_run)}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
