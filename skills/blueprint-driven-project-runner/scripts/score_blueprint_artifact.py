#!/usr/bin/env python3
"""Score blueprint-runner artifacts against the execution contract.

Examples:
  python score_blueprint_artifact.py --path blueprint-output.md
  python score_blueprint_artifact.py --path goal-prompt.md --mode goal --strict
  python score_blueprint_artifact.py --path execution-contract.md --json
"""

from __future__ import annotations

import argparse
import json
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

LEDGER_HEADERS = [
    "ID",
    "Blueprint Records",
    "Work Slice",
    "Goal",
    "Completion Path",
    "Acceptance Standard",
    "Verification Method",
    "Status",
    "Accepted?",
]

GOAL_SECTIONS = [
    "First Principle",
    "Read First",
    "Blueprint Records",
    "Work Slice",
    "Execution Ledger",
    "Allowed Changes",
    "Forbidden Changes",
    "Verification Plan",
    "Evidence Required",
    "Stop Conditions",
]

CONTRACT_TERMS = [
    "Blueprint Record",
    "Work Slice",
    "Execution Ledger",
    "Allowed",
    "Forbidden",
    "Verification",
    "Evidence",
    "Stop",
]

BAD_BROAD_PHRASES = [
    "continue optimizing",
    "improve generally",
    "fix anything you notice",
    "make the whole module mature",
    "refactor as needed",
    "optimize as much as possible",
    "use your judgment to complete adjacent issues",
    "\u7ee7\u7eed\u4f18\u5316",
    "\u5168\u9762\u5b8c\u5584",
    "\u987a\u624b\u4fee",
    "\u5c3d\u91cf\u505a\u597d",
    "\u81ea\u7531\u53d1\u6325",
]

GROUNDING_CHECKS = [
    ("source evidence", ["Source evidence", "Source:"]),
    ("current state", ["Current state", "Current Evidence:"]),
    ("observable target", ["Observable target", "Target Behavior:"]),
    ("forbidden outcomes", ["Forbidden outcomes", "Forbidden Result:"]),
    ("user-checkable preview", ["User-checkable preview", "Preview:"]),
    ("pass/fail acceptance", ["Pass/fail acceptance", "Acceptance:"]),
    ("verification method", ["Verification method", "Verification:"]),
    ("decision path", ["DECISION_NEEDED", "Open Questions:", "needs-decision"]),
    ("execution allowed", ["Execution allowed", "Status: ready", "Status: accepted", "Discovery brief only"]),
]

RECORD_ID_RE = re.compile(r"\b[A-Z][A-Z0-9]*(?:[-_][A-Z0-9]+)+-\d{3,}\b")


@dataclass
class Check:
    name: str
    passed: bool
    detail: str
    severity: str = "error"


def table_has_headers(text: str, headers: list[str]) -> bool:
    table_lines = [line for line in text.splitlines() if line.strip().startswith("|")]
    for line in table_lines:
        cells = [cell.strip().lower() for cell in line.strip().strip("|").split("|")]
        if sum(1 for header in headers if header.lower() in cells) >= max(5, len(headers) - 2):
            return True
    return False


def detect_mode(text: str) -> str:
    lowered = text.lower()
    if "goal prompt" in lowered or "first principle" in lowered:
        return "goal"
    if "execution contract" in lowered or "contract id" in lowered:
        return "contract"
    return "blueprint"


def grounding_result(text: str) -> tuple[int, list[str]]:
    lowered = text.lower()
    missing: list[str] = []
    hits = 0
    for name, options in GROUNDING_CHECKS:
        if any(option.lower() in lowered for option in options):
            hits += 1
        else:
            missing.append(name)
    return hits, missing


def blueprint_checks(text: str) -> list[Check]:
    checks: list[Check] = []
    missing_fields = [field for field in FIELD_NAMES if f"{field}:" not in text]
    found_record_id = bool(RECORD_ID_RE.search(text))
    grounding_hits, missing_grounding = grounding_result(text)
    checks.append(Check("executable-record-fields", not missing_fields, f"missing fields: {', '.join(missing_fields) or 'none'}"))
    checks.append(Check("stable-record-id", found_record_id, "found stable record ID" if found_record_id else "no stable record ID found"))
    checks.append(Check("grounding-preflight", grounding_hits >= 7, f"missing grounding checks: {', '.join(missing_grounding) or 'none'}"))
    checks.append(Check("preview-acceptance-verification", all(term in text for term in ["Preview:", "Acceptance:", "Verification:"]), "record has preview, acceptance, and verification"))
    checks.append(Check("ledger-queue", "Execution Ledger" in text and table_has_headers(text, LEDGER_HEADERS), "output includes an execution ledger task table"))
    checks.append(Check("blocking-or-decision-path", any(term in text for term in ["DECISION_NEEDED", "blocked", "shelved", "decision queue", "Open Questions"]), "output names how unresolved work is handled", "warn"))
    return checks


def goal_checks(text: str) -> list[Check]:
    checks: list[Check] = []
    missing_sections = [section for section in GOAL_SECTIONS if section.lower() not in text.lower()]
    checks.append(Check("goal-sections", not missing_sections, f"missing sections: {', '.join(missing_sections) or 'none'}"))
    first_principle = re.search(r"##\s+First Principle(.+?)(?:\n##\s+|\Z)", text, re.DOTALL | re.IGNORECASE)
    first_text = first_principle.group(1) if first_principle else ""
    checks.append(Check("first-principle-binds-ledger", "blueprint" in first_text.lower() and "ledger" in first_text.lower(), "first principle binds blueprint records and ledger rows"))
    checks.append(Check("ledger-row-ids", bool(re.search(r"\bLEDGER[-_][A-Z0-9_-]*\d+\b", text, re.IGNORECASE)) or "Rows:" in text, "goal prompt cites ledger rows"))
    checks.append(Check("scope-controls", "Allowed" in text and "Forbidden" in text, "goal prompt has allowed and forbidden scope"))
    checks.append(Check("shelve-not-stall", any(term in text.lower() for term in ["shelved", "shelve", "blocked", "resume condition"]), "goal prompt allows blocked rows to be shelved instead of stopping all work", "warn"))
    return checks


def contract_checks(text: str) -> list[Check]:
    checks: list[Check] = []
    missing_terms = [term for term in CONTRACT_TERMS if term.lower() not in text.lower()]
    checks.append(Check("contract-terms", not missing_terms, f"missing terms: {', '.join(missing_terms) or 'none'}"))
    checks.append(Check("ledger-row-scope", "Ledger Row" in text or "Execution Ledger Row" in text, "contract names ledger row IDs"))
    checks.append(Check("evidence-stop", "Evidence" in text and "Stop" in text, "contract has evidence and stop condition"))
    return checks


def shared_checks(text: str) -> list[Check]:
    found_bad = [phrase for phrase in BAD_BROAD_PHRASES if phrase.lower() in text.lower()]
    return [
        Check("no-broad-goal-phrases", not found_bad, f"broad phrases: {', '.join(found_bad) or 'none'}"),
        Check("not-summary-only", len(text.splitlines()) >= 20 and ("Acceptance" in text or "Verification" in text), "artifact is more than a short prose summary"),
    ]


def score(path: Path, mode: str) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    actual_mode = detect_mode(text) if mode == "auto" else mode
    checks = shared_checks(text)
    if actual_mode == "blueprint":
        checks.extend(blueprint_checks(text))
    elif actual_mode == "goal":
        checks.extend(goal_checks(text))
    elif actual_mode == "contract":
        checks.extend(contract_checks(text))
    else:
        raise ValueError(f"unknown mode: {mode}")

    errors = [check for check in checks if not check.passed and check.severity == "error"]
    warnings = [check for check in checks if not check.passed and check.severity == "warn"]
    passed = sum(1 for check in checks if check.passed)
    return {
        "path": str(path),
        "mode": actual_mode,
        "passed": passed,
        "total": len(checks),
        "errors": len(errors),
        "warnings": len(warnings),
        "checks": [check.__dict__ for check in checks],
    }


def render_markdown(result: dict[str, object]) -> str:
    lines = [
        "# Blueprint Artifact Score",
        "",
        f"Path: `{result['path']}`",
        f"Mode: `{result['mode']}`",
        f"Score: {result['passed']} / {result['total']}",
        f"Errors: {result['errors']}",
        f"Warnings: {result['warnings']}",
        "",
        "| Check | Result | Severity | Detail |",
        "| --- | --- | --- | --- |",
    ]
    for check in result["checks"]:  # type: ignore[index]
        status = "pass" if check["passed"] else "fail"
        lines.append(f"| {check['name']} | {status} | {check['severity']} | {check['detail']} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Score blueprint-runner generated artifacts.")
    parser.add_argument("--path", required=True, help="Markdown artifact to score")
    parser.add_argument("--mode", choices=["auto", "blueprint", "goal", "contract"], default="auto")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero when error checks fail")
    args = parser.parse_args()

    result = score(Path(args.path).resolve(), args.mode)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(result))
    return 1 if args.strict and result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
