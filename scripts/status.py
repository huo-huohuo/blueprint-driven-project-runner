#!/usr/bin/env python3
"""Show project status for Blueprint Governance.

Examples:
  python status.py --project C:/repo
  python status.py --project . --json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


FIELD_RE = re.compile(
    r"^(ID|Type|Source|Current Evidence|Target Behavior|Forbidden Result|Preview|Acceptance|Verification|Owner|Status|Confidence|Open Questions):\s*(.*)$"
)
HILL_VALUES = {"raw", "shaped", "validated", "executing", "verified", "accepted"}
LEDGER_STATUSES = {"planned", "active", "blocked", "shelved", "skipped", "verified", "accepted"}


def slug(value: str) -> str:
    chars = [ch.lower() if ch.isalnum() else "-" for ch in value.strip()]
    result = "".join(chars)
    while "--" in result:
        result = result.replace("--", "-")
    return result.strip("-") or "module"


def compact(lines: list[str]) -> str:
    return " ".join(line.strip() for line in lines if line.strip()).strip()


def parse_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    current: dict[str, list[str]] | None = None
    current_field: str | None = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip().lstrip("\ufeff")
        match = FIELD_RE.match(line)
        if match:
            field = match.group(1)
            value = match.group(2).strip()
            if field == "ID":
                if current:
                    current["_path"] = [str(path)]
                    records.append(current)
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
        records.append(current)
    return records


def module_from_path(ai_control: Path, path: Path) -> str:
    try:
        rel = path.relative_to(ai_control)
    except ValueError:
        return "(unknown)"
    parts = rel.parts
    if len(parts) > 1 and parts[0] not in {"decisions"}:
        return parts[0]
    return "(root)"


def blueprint_files(ai_control: Path) -> list[Path]:
    if not ai_control.exists():
        return []
    return sorted(path for path in ai_control.rglob("*.md") if "blueprint" in path.name.lower())


def goal_prompt_files(ai_control: Path) -> list[Path]:
    if not ai_control.exists():
        return []
    files = list(ai_control.rglob("goal-prompts/*.md"))
    files.extend(path for path in ai_control.rglob("*goal*.md") if "goal-prompts" not in str(path))
    return sorted(set(files))


def parse_markdown_table(lines: list[str]) -> list[dict[str, str]]:
    header: list[str] | None = None
    rows: list[dict[str, str]] = []
    for raw in lines:
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells:
            continue
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        if header is None:
            header = cells
            continue
        padded = cells + [""] * max(0, len(header) - len(cells))
        rows.append(dict(zip(header, padded)))
    return rows


def parse_execution_ledger(ai_control: Path) -> dict[str, Any]:
    path = ai_control / "91-execution-ledger.md"
    result: dict[str, Any] = {
        "exists": path.exists(),
        "path": str(path),
        "rows": 0,
        "statuses": Counter(),
        "accepted": 0,
        "open": 0,
    }
    if not path.exists():
        return result

    task_lines: list[str] = []
    in_task_queue = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if stripped.startswith("## "):
            in_task_queue = stripped.lower() == "## task queue"
            continue
        if in_task_queue:
            task_lines.append(raw)

    rows = parse_markdown_table(task_lines)
    for row in rows:
        row_id = row.get("ID", "").strip()
        if not row_id or row_id.lower() == "id":
            continue
        status = row.get("Status", "").strip().lower() or "unknown"
        accepted = row.get("Accepted?", "").strip().lower()
        if status not in LEDGER_STATUSES:
            status = status or "unknown"
        result["rows"] += 1
        result["statuses"][status] += 1
        if status == "accepted" or accepted in {"yes", "y", "true"}:
            result["accepted"] += 1
        elif status not in {"skipped"}:
            result["open"] += 1

    result["statuses"] = dict(result["statuses"])
    return result


def parse_work_slices(ai_control: Path) -> list[dict[str, str]]:
    slices: list[dict[str, str]] = []
    for path in sorted(ai_control.rglob("work-slices.md")):
        module = module_from_path(ai_control, path)
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line.startswith("|") or "WS-" not in line:
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if not cells or not cells[0].startswith("WS-"):
                continue
            hill = next((cell for cell in cells if cell in HILL_VALUES), "")
            slices.append({"module": module, "id": cells[0], "hill": hill or "unknown", "path": str(path)})
    return slices


def build_status(root: Path) -> dict[str, Any]:
    ai_control = root / "docs" / "ai-control"
    records: list[dict[str, Any]] = []
    modules: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "records": 0,
        "statuses": Counter(),
        "types": Counter(),
        "decision_needed": 0,
        "evidence_pending": 0,
        "goal_prompts": 0,
        "work_slices": 0,
        "executing_slices": 0,
    })

    for path in blueprint_files(ai_control):
        module = module_from_path(ai_control, path)
        for record in parse_records(path):
            record_id = compact(record.get("ID", []))
            if not record_id:
                continue
            status = compact(record.get("Status", [])).lower() or "unknown"
            record_type = compact(record.get("Type", [])).lower() or "unknown"
            combined = "\n".join(compact(record.get(field, [])) for field in record.keys() if isinstance(record.get(field), list))
            record["_module"] = module
            records.append(record)

            modules[module]["records"] += 1
            modules[module]["statuses"][status] += 1
            modules[module]["types"][record_type] += 1
            if "DECISION_NEEDED" in combined or status in {"draft", "needs-decision", "unknown"}:
                modules[module]["decision_needed"] += 1
            if status == "ready":
                modules[module]["evidence_pending"] += 1

    for path in goal_prompt_files(ai_control):
        module = module_from_path(ai_control, path)
        modules[module]["goal_prompts"] += 1

    work_slices = parse_work_slices(ai_control)
    execution_ledger = parse_execution_ledger(ai_control)
    for item in work_slices:
        module = item["module"]
        modules[module]["work_slices"] += 1
        if item["hill"] == "executing":
            modules[module]["executing_slices"] += 1

    all_statuses = Counter()
    all_types = Counter()
    for data in modules.values():
        all_statuses.update(data["statuses"])
        all_types.update(data["types"])

    summary = {
        "project": str(root),
        "ai_control_exists": ai_control.exists(),
        "blueprint_files": len(blueprint_files(ai_control)),
        "records": len(records),
        "statuses": dict(all_statuses),
        "types": dict(all_types),
        "goal_prompts": len(goal_prompt_files(ai_control)),
        "work_slices": len(work_slices),
        "executing_slices": sum(1 for item in work_slices if item["hill"] == "executing"),
        "execution_ledger_exists": execution_ledger["exists"],
        "execution_ledger_rows": execution_ledger["rows"],
        "execution_ledger_statuses": execution_ledger["statuses"],
        "execution_ledger_accepted": execution_ledger["accepted"],
        "execution_ledger_open": execution_ledger["open"],
        "decision_needed": sum(data["decision_needed"] for data in modules.values()),
        "evidence_pending": sum(data["evidence_pending"] for data in modules.values()),
    }

    normalized_modules = {}
    for module, data in sorted(modules.items()):
        normalized_modules[module] = {
            "records": data["records"],
            "statuses": dict(data["statuses"]),
            "types": dict(data["types"]),
            "decision_needed": data["decision_needed"],
            "evidence_pending": data["evidence_pending"],
            "goal_prompts": data["goal_prompts"],
            "work_slices": data["work_slices"],
            "executing_slices": data["executing_slices"],
        }

    return {"summary": summary, "modules": normalized_modules, "execution_ledger": execution_ledger}


def render_markdown(status: dict[str, Any]) -> str:
    summary = status["summary"]
    modules = status["modules"]

    lines = [
        "# AI Control Status",
        "",
        f"Project: `{summary['project']}`",
        f"AI control installed: `{summary['ai_control_exists']}`",
        "",
        "## Summary",
        "",
        f"- Blueprint files: {summary['blueprint_files']}",
        f"- Blueprint records: {summary['records']}",
        f"- Statuses: {summary['statuses']}",
        f"- Goal prompts: {summary['goal_prompts']}",
        f"- Work slices: {summary['work_slices']}",
        f"- Executing slices: {summary['executing_slices']}",
        f"- Execution ledger installed: {summary['execution_ledger_exists']}",
        f"- Execution ledger rows: {summary['execution_ledger_rows']}",
        f"- Execution ledger statuses: {summary['execution_ledger_statuses']}",
        f"- Execution ledger accepted/open: {summary['execution_ledger_accepted']} / {summary['execution_ledger_open']}",
        f"- Decision needed / blockers: {summary['decision_needed']}",
        f"- Evidence pending: {summary['evidence_pending']}",
        "",
        "## Modules",
        "",
        "| Module | Records | Ready | Accepted | Draft | Needs Decision | Goal Prompts | Work Slices | Executing | Evidence Pending |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for module, data in modules.items():
        statuses = data["statuses"]
        lines.append(
            "| {module} | {records} | {ready} | {accepted} | {draft} | {needs} | {goals} | {slices} | {executing} | {pending} |".format(
                module=module,
                records=data["records"],
                ready=statuses.get("ready", 0),
                accepted=statuses.get("accepted", 0),
                draft=statuses.get("draft", 0),
                needs=statuses.get("needs-decision", 0),
                goals=data["goal_prompts"],
                slices=data["work_slices"],
                executing=data["executing_slices"],
                pending=data["evidence_pending"],
            )
        )

    lines.extend([
        "",
        "## Suggested Next Move",
        "",
    ])
    if not summary["ai_control_exists"]:
        lines.append("- Install the governance system first.")
    elif summary["decision_needed"]:
        lines.append("- Resolve `DECISION_NEEDED`, draft, or needs-decision records before execution.")
    elif summary["evidence_pending"] and not summary["execution_ledger_rows"]:
        lines.append("- Compile the execution ledger before starting a long-running goal.")
    elif summary["evidence_pending"] and not summary["goal_prompts"]:
        lines.append("- Generate goal prompts for ready records.")
    elif summary["executing_slices"]:
        lines.append("- Continue execution only against the active work slice and collect evidence.")
    elif summary["evidence_pending"]:
        lines.append("- Start a bounded execution from a generated goal prompt.")
    else:
        lines.append("- No obvious blockers from the project status scan.")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Show Blueprint Governance project status.")
    parser.add_argument("--project", required=True, help="Project root")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    root = Path(args.project).resolve()
    status = build_status(root)
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(status))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
