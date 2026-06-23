#!/usr/bin/env python3
"""Lint executable blueprint records for readiness.

Examples:
  python lint_blueprints.py --project C:/repo
  python lint_blueprints.py --path C:/repo/docs/ai-control/module/engineering-blueprint.md
  python lint_blueprints.py --project . --advisory
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
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
WEAK_VALUES = {"", "-", "tbd", "todo", "n/a", "none"}
TECHNICAL_TYPES = {"engineering", "data", "integration", "automation", "infrastructure", "safety", "ops"}
DETAIL_FIELDS = ["Target Behavior", "Preview", "Acceptance", "Verification"]
TECHNICAL_PREVIEW_TERMS = [
    "business flow",
    "before/after",
    "input/output",
    "state",
    "boundary",
    "failure",
    "evidence",
    "业务",
    "前后",
    "输入",
    "输出",
    "状态",
    "边界",
    "失败",
    "证据",
]
VAGUE_WORDS = [
    "optimize",
    "improve",
    "better",
    "smart",
    "intelligent",
    "mature",
    "clean",
    "professional",
    "complete",
    "comprehensive",
    "robust",
    "easy",
    "convenient",
    "clear",
    "优化",
    "完善",
    "更好",
    "智能",
    "成熟",
    "清晰",
    "高效",
    "方便",
    "美观",
    "专业",
    "完整",
    "全面",
    "稳定",
]

FIELD_RE = re.compile(
    r"^(ID|Type|Source|Current Evidence|Target Behavior|Forbidden Result|Preview|Acceptance|Verification|Owner|Status|Confidence|Open Questions):\s*(.*)$"
)


@dataclass
class Issue:
    severity: str
    path: Path
    message: str


def compact(lines: list[str]) -> str:
    return " ".join(line.strip() for line in lines if line.strip()).strip()


def weak(value: str) -> bool:
    cleaned = value.strip().strip("-").strip().lower()
    return cleaned in WEAK_VALUES


def detail_score(value: str) -> int:
    tokens = re.findall(r"[A-Za-z0-9_\-/]+|[\u4e00-\u9fff]", value)
    return len(tokens)


def parse_records(text: str) -> list[dict[str, list[str]]]:
    records: list[dict[str, list[str]]] = []
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
        records.append(current)
    return records


def markdown_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    if not target.exists():
        return []
    return sorted(path for path in target.rglob("*.md") if "blueprint" in path.name.lower())


def lint_file(path: Path) -> tuple[int, list[Issue]]:
    text = path.read_text(encoding="utf-8")
    records = parse_records(text)
    issues: list[Issue] = []

    if not records:
        issues.append(Issue("ERROR", path, "no executable blueprint records found; this looks like a summary or empty blueprint file"))
        return 0, issues

    for index, record in enumerate(records, start=1):
        label = compact(record.get("ID", [])) or f"record {index}"
        for field in FIELD_NAMES:
            value = compact(record.get(field, []))
            if field not in record:
                issues.append(Issue("ERROR", path, f"{label}: missing required field {field}"))
            elif weak(value):
                issues.append(Issue("ERROR", path, f"{label}: empty or weak field {field}"))

        status = compact(record.get("Status", [])).lower()
        if status and status not in READY_STATUSES:
            issues.append(Issue("ERROR", path, f"{label}: status is {status!r}, not ready/accepted"))

        combined = "\n".join(compact(record.get(field, [])) for field in FIELD_NAMES)
        if "DECISION_NEEDED" in combined:
            issues.append(Issue("ERROR", path, f"{label}: contains DECISION_NEEDED, so it cannot authorize execution"))

        if "NOT_CHECKED" in compact(record.get("Current Evidence", [])):
            issues.append(Issue("WARN", path, f"{label}: current evidence is NOT_CHECKED"))

        for field in DETAIL_FIELDS:
            value = compact(record.get(field, []))
            if not weak(value) and "DECISION_NEEDED" not in value and detail_score(value) < 8:
                issues.append(Issue("WARN", path, f"{label}: {field} looks too thin for reliable execution"))

        record_type = compact(record.get("Type", [])).lower()
        preview = compact(record.get("Preview", []))
        if record_type in TECHNICAL_TYPES:
            found_terms = {term for term in TECHNICAL_PREVIEW_TERMS if term.lower() in preview.lower()}
            if len(found_terms) < 3:
                issues.append(
                    Issue(
                        "WARN",
                        path,
                        f"{label}: technical preview should include checklist/sample elements such as business flow, before/after, state, boundaries, failure, and evidence",
                    )
                )

        lower_combined = combined.lower()
        found_vague = [word for word in VAGUE_WORDS if word.lower() in lower_combined]
        if found_vague:
            unique = ", ".join(sorted(set(found_vague)))
            issues.append(Issue("WARN", path, f"{label}: vague words need measurable criteria: {unique}"))

    return len(records), issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint executable blueprint records.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--project", help="Project root; lints docs/ai-control/**/*blueprint*.md")
    group.add_argument("--path", help="Specific blueprint file or directory")
    parser.add_argument("--advisory", action="store_true", help="Always exit 0 after reporting issues")
    args = parser.parse_args()

    target = Path(args.path).resolve() if args.path else Path(args.project).resolve() / "docs" / "ai-control"
    files = markdown_files(target)

    if not files:
        print(f"ERROR: no blueprint markdown files found under {target}")
        return 0 if args.advisory else 1

    total_records = 0
    all_issues: list[Issue] = []
    for path in files:
        count, issues = lint_file(path)
        total_records += count
        all_issues.extend(issues)

    for issue in all_issues:
        print(f"{issue.severity}: {issue.path}: {issue.message}")

    errors = sum(1 for issue in all_issues if issue.severity == "ERROR")
    warnings = sum(1 for issue in all_issues if issue.severity == "WARN")
    print(f"SUMMARY: files={len(files)} records={total_records} errors={errors} warnings={warnings}")

    if args.advisory:
        return 0
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
