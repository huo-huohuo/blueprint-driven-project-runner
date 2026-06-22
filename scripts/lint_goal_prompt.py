#!/usr/bin/env python3
"""Lint goal prompts for blueprint-bound execution.

Examples:
  python lint_goal_prompt.py --project C:/repo
  python lint_goal_prompt.py --path C:/repo/docs/ai-control/module/goal-prompts/task.md --project C:/repo
  python lint_goal_prompt.py --path task.md --advisory
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


FIELD_RE = re.compile(
    r"^(ID|Type|Source|Current Evidence|Target Behavior|Forbidden Result|Preview|Acceptance|Verification|Owner|Status|Confidence|Open Questions):\s*(.*)$"
)
RECORD_ID_RE = re.compile(r"\b[A-Z][A-Z0-9]*(?:[-_][A-Z0-9]+)+-\d{3,}\b")
REQUIRED_SECTIONS = [
    "First Principle",
    "Read First",
    "Blueprint Records",
    "Work Slice",
    "Allowed Changes",
    "Forbidden Changes",
    "Data Policy",
    "Verification Plan",
    "Evidence Required In Final Response",
    "Stop Conditions",
    "Unexpected Discoveries",
]
BAD_PHRASES = [
    "improve generally",
    "continue optimizing",
    "fix anything you notice",
    "make the whole module mature",
    "refactor as needed",
    "optimize as much as possible",
    "use your judgment to complete adjacent issues",
    "继续优化",
    "全面完善",
    "顺手修",
    "尽量做好",
    "自由发挥",
]
READY_STATUSES = {"ready", "accepted"}


@dataclass
class Issue:
    severity: str
    path: Path
    message: str


def compact(lines: list[str]) -> str:
    return " ".join(line.strip() for line in lines if line.strip()).strip()


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = ""
    for raw in text.splitlines():
        line = raw.strip().lstrip("\ufeff")
        if line.startswith("## "):
            current = line.lstrip("#").strip()
            sections[current] = []
            continue
        if current:
            sections[current].append(raw)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def parse_records(path: Path) -> dict[str, dict[str, list[str]]]:
    records: dict[str, dict[str, list[str]]] = {}
    if not path.exists():
        return records
    for md in sorted(path.rglob("*blueprint*.md")):
        current: dict[str, list[str]] | None = None
        current_field: str | None = None
        for raw in md.read_text(encoding="utf-8").splitlines():
            line = raw.strip().lstrip("\ufeff")
            match = FIELD_RE.match(line)
            if match:
                field = match.group(1)
                value = match.group(2).strip()
                if field == "ID":
                    if current and compact(current.get("ID", [])):
                        records[compact(current.get("ID", []))] = current
                    current = {}
                if current is None:
                    current = {}
                current[field] = [value] if value else []
                current_field = field
                continue
            if current is not None and current_field and line:
                current[current_field].append(line)
        if current and compact(current.get("ID", [])):
            records[compact(current.get("ID", []))] = current
    return records


def goal_prompt_files(project: Path) -> list[Path]:
    ai_control = project / "docs" / "ai-control"
    files = list(ai_control.rglob("goal-prompts/*.md")) if ai_control.exists() else []
    files.extend(path for path in ai_control.rglob("*goal*.md") if ai_control.exists() and "goal-prompts" not in str(path))
    return sorted(set(files))


def lint_file(path: Path, project: Path | None) -> list[Issue]:
    text = path.read_text(encoding="utf-8")
    sections = parse_sections(text)
    issues: list[Issue] = []

    for section in REQUIRED_SECTIONS:
        if section not in sections:
            issues.append(Issue("ERROR", path, f"missing required section: {section}"))
        elif not sections[section].strip():
            issues.append(Issue("ERROR", path, f"empty required section: {section}"))

    first_principle = sections.get("First Principle", "")
    if "Complete the referenced executable blueprint records exactly" not in first_principle:
        issues.append(Issue("ERROR", path, "first principle must require exact blueprint completion"))

    if "DECISION_NEEDED" in text:
        issues.append(Issue("ERROR", path, "contains DECISION_NEEDED"))

    lower = text.lower()
    for phrase in BAD_PHRASES:
        if phrase.lower() in lower:
            issues.append(Issue("ERROR", path, f"contains forbidden broad goal phrase: {phrase}"))

    blueprint_section = sections.get("Blueprint Records", "")
    record_ids = sorted(set(RECORD_ID_RE.findall(blueprint_section)))
    if not record_ids:
        issues.append(Issue("ERROR", path, "no blueprint record IDs found"))

    if project:
        records = parse_records(project / "docs" / "ai-control")
        for record_id in record_ids:
            record = records.get(record_id)
            if not record:
                issues.append(Issue("ERROR", path, f"referenced blueprint record not found: {record_id}"))
                continue
            status = compact(record.get("Status", [])).lower()
            combined = "\n".join(compact(record.get(field, [])) for field in record)
            if status not in READY_STATUSES:
                issues.append(Issue("ERROR", path, f"referenced record {record_id} is {status!r}, not ready/accepted"))
            if "DECISION_NEEDED" in combined:
                issues.append(Issue("ERROR", path, f"referenced record {record_id} contains DECISION_NEEDED"))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint blueprint-derived goal prompts.")
    parser.add_argument("--project", help="Project root; required to validate referenced blueprint records")
    parser.add_argument("--path", help="Specific goal prompt file")
    parser.add_argument("--advisory", action="store_true", help="Always exit 0 after reporting issues")
    args = parser.parse_args()

    project = Path(args.project).resolve() if args.project else None
    if args.path:
        files = [Path(args.path).resolve()]
    elif project:
        files = goal_prompt_files(project)
    else:
        raise SystemExit("ERROR: provide --project or --path")

    if not files:
        print("ERROR: no goal prompt files found")
        return 0 if args.advisory else 1

    all_issues: list[Issue] = []
    for path in files:
        all_issues.extend(lint_file(path, project))

    for issue in all_issues:
        print(f"{issue.severity}: {issue.path}: {issue.message}")

    errors = sum(1 for issue in all_issues if issue.severity == "ERROR")
    warnings = sum(1 for issue in all_issues if issue.severity == "WARN")
    print(f"SUMMARY: files={len(files)} errors={errors} warnings={warnings}")

    if args.advisory:
        return 0
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
