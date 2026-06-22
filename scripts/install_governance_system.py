#!/usr/bin/env python3
"""Install the Blueprint Governance System into a target project.

Examples:
  python install_governance_system.py --project C:/repo
  python install_governance_system.py --project . --module "Inventory" --module "Reporting"
  python install_governance_system.py --project . --dry-run
"""

from __future__ import annotations

import argparse
from pathlib import Path

from scaffold_control_pack import DEFAULT_MODULES, collect_outputs


START = "<!-- BLUEPRINT-GOVERNANCE:START -->"
END = "<!-- BLUEPRINT-GOVERNANCE:END -->"


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def read_skill_file(relative: str) -> str:
    return (skill_root() / relative).read_text(encoding="utf-8")


def write_file(path: Path, content: str, overwrite: bool, dry_run: bool) -> str:
    if path.exists() and not overwrite:
        return "exists"
    if dry_run:
        return "would-write"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return "written"


def governance_agents_block() -> str:
    return f"""{START}

# Blueprint Governance

For large or long-running AI-assisted work, follow the project operating standard in `docs/ai-control/00-operating-standard.md`.

Core rules:

- No executable blueprint, no implementation.
- A summary, PRD paragraph, or feature list cannot authorize broad code changes.
- Broad work requires ready executable blueprint records and an execution contract.
- Technical/backend records require user-checkable previews such as checklists, before/after examples, state tables, boundaries, failure matrices, and evidence plans.
- Before long-running execution, generate a goal prompt from ready blueprint records; blueprint completion is the first principle.
- Run `python tools/ai-control/lint_blueprints.py --project .` before Execution mode when blueprint files exist.
- Use `python tools/ai-control/generate_goal_prompt.py --project . --module "<module>" --record "<record-id>"` to create goal-mode prompts.
- Use `python tools/ai-control/status.py --project .` to inspect project progress.
- Use `python tools/ai-control/lint_goal_prompt.py --project .` before starting a generated goal prompt.
- Use `python tools/ai-control/generate_handoff_package.py --project . --module "<module>" --record "<record-id>" --work-slice "<slice-id>"` to start a fresh thread with bounded context.
- Do not perform high-risk actions without explicit user confirmation: external side effects, production-like writes, deletion, schema or migration changes, access-control changes, deployment changes, background cursor or offset mutation, or bulk automated actions.
- If work drifts, stop implementation, classify changed files, and update `docs/ai-control/92-drift-log.md`.

{END}
"""


def update_agents(path: Path, dry_run: bool) -> str:
    block = governance_agents_block()
    if not path.exists():
        if dry_run:
            return "would-write"
        path.write_text(block, encoding="utf-8", newline="\n")
        return "written"

    text = path.read_text(encoding="utf-8")
    if START in text and END in text:
        before = text.split(START, 1)[0].rstrip()
        after = text.split(END, 1)[1].lstrip()
        new_text = f"{before}\n\n{block.rstrip()}\n\n{after}".rstrip() + "\n"
        if dry_run:
            return "would-refresh-marker"
        path.write_text(new_text, encoding="utf-8", newline="\n")
        return "refreshed-marker"

    new_text = text.rstrip() + "\n\n" + block
    if dry_run:
        return "would-append-marker"
    path.write_text(new_text, encoding="utf-8", newline="\n")
    return "appended-marker"


def preflight_doc() -> str:
    return """# Blueprint Governance Preflight

Run this before broad implementation.

## Required Checks

- Project root confirmed.
- `AGENTS.md` read.
- `docs/ai-control/00-operating-standard.md` read.
- Relevant module blueprints read.
- Blueprint records are `ready` or `accepted`.
- Execution contract exists.
- Allowed files and forbidden files are explicit.
- Data-write policy is explicit.
- Verification plan is explicit.
- High-risk actions have explicit user confirmation.
- Goal prompt is generated from ready blueprint records before long-running execution.
- Goal prompt passes lint before target-mode execution.
- Handoff package exists for new long-running module threads.

## Command

```bash
python tools/ai-control/status.py --project .
python tools/ai-control/lint_blueprints.py --project .
python tools/ai-control/generate_goal_prompt.py --project . --module "<module>" --record "<record-id>"
python tools/ai-control/lint_goal_prompt.py --project .
python tools/ai-control/generate_handoff_package.py --project . --module "<module>" --record "<record-id>" --work-slice "<slice-id>"
```

If the linter reports errors, do not enter Execution mode.
"""


def install(root: Path, modules: list[str], out: str, overwrite: bool, dry_run: bool, no_agents: bool, no_tools: bool) -> list[tuple[Path, str]]:
    out_dir = root / out
    results: list[tuple[Path, str]] = []

    if not no_agents:
        results.append((root / "AGENTS.md", update_agents(root / "AGENTS.md", dry_run)))

    operating_standard = read_skill_file("references/project-operating-standard.md")
    results.append((out_dir / "00-operating-standard.md", write_file(out_dir / "00-operating-standard.md", operating_standard, overwrite, dry_run)))

    for path, status in collect_outputs(root, out_dir, modules, overwrite, dry_run):
        results.append((path, status))

    results.append((out_dir / "93-preflight-checklist.md", write_file(out_dir / "93-preflight-checklist.md", preflight_doc(), overwrite, dry_run)))

    if not no_tools:
        linter = read_skill_file("scripts/lint_blueprints.py")
        results.append((root / "tools" / "ai-control" / "lint_blueprints.py", write_file(root / "tools" / "ai-control" / "lint_blueprints.py", linter, overwrite, dry_run)))
        generator = read_skill_file("scripts/generate_goal_prompt.py")
        results.append((root / "tools" / "ai-control" / "generate_goal_prompt.py", write_file(root / "tools" / "ai-control" / "generate_goal_prompt.py", generator, overwrite, dry_run)))
        status = read_skill_file("scripts/status.py")
        results.append((root / "tools" / "ai-control" / "status.py", write_file(root / "tools" / "ai-control" / "status.py", status, overwrite, dry_run)))
        goal_linter = read_skill_file("scripts/lint_goal_prompt.py")
        results.append((root / "tools" / "ai-control" / "lint_goal_prompt.py", write_file(root / "tools" / "ai-control" / "lint_goal_prompt.py", goal_linter, overwrite, dry_run)))
        handoff = read_skill_file("scripts/generate_handoff_package.py")
        results.append((root / "tools" / "ai-control" / "generate_handoff_package.py", write_file(root / "tools" / "ai-control" / "generate_handoff_package.py", handoff, overwrite, dry_run)))

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Blueprint Governance into a project.")
    parser.add_argument("--project", required=True, help="Project root")
    parser.add_argument("--module", action="append", dest="modules", help="Module name; may repeat")
    parser.add_argument("--out", default="docs/ai-control", help="Output directory relative to project root")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing generated files")
    parser.add_argument("--dry-run", action="store_true", help="Print planned writes without changing files")
    parser.add_argument("--no-agents", action="store_true", help="Do not create or update AGENTS.md")
    parser.add_argument("--no-tools", action="store_true", help="Do not copy tools/ai-control/lint_blueprints.py")
    args = parser.parse_args()

    root = Path(args.project).resolve()
    modules = args.modules or DEFAULT_MODULES

    for path, status in install(root, modules, args.out, args.overwrite, args.dry_run, args.no_agents, args.no_tools):
        print(f"{status}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
