# Blueprint-Driven Project Runner for Codex

A Codex skill and lightweight governance toolkit for running large AI-assisted projects with executable blueprints, bounded goal prompts, verification gates, and thread handoff packages.

This is for projects where ordinary long-running AI goals become vague, repetitive, or risky. The skill forces the work to start from concrete blueprint records, then generates narrow execution prompts and handoff packages that can be validated.

## What It Provides

- Executable blueprint records with source evidence, target behavior, forbidden results, previews, acceptance criteria, and verification plans.
- Goal prompt generation that binds execution to specific blueprint record IDs.
- Goal prompt linting to catch broad or unsafe instructions such as "continue optimizing" or "fix anything you notice".
- Project status reporting across blueprints, work slices, blockers, and generated prompts.
- Thread handoff packages so a fresh Codex thread can continue work without relying on hidden chat history.
- A project governance installer that adds `docs/ai-control` and `tools/ai-control` to a target repository.

## Repository Layout

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── blueprint-examples.md
│   ├── goal-prompt-protocol.md
│   ├── project-operating-standard.md
│   ├── quality-bars.md
│   ├── technical-blueprint-questionnaire.md
│   └── templates.md
├── scripts/
│   ├── generate_goal_prompt.py
│   ├── generate_handoff_package.py
│   ├── install_governance_system.py
│   ├── lint_blueprints.py
│   ├── lint_goal_prompt.py
│   ├── scaffold_control_pack.py
│   └── status.py
└── examples/
```

## Install As A Codex Skill

Clone this repository into your Codex skills directory:

```bash
git clone https://github.com/huo-huohuo/blueprint-driven-project-runner.git ~/.codex/skills/blueprint-driven-project-runner
```

On Windows PowerShell:

```powershell
git clone https://github.com/huo-huohuo/blueprint-driven-project-runner.git "$env:USERPROFILE\.codex\skills\blueprint-driven-project-runner"
```

Restart Codex or reload skills if needed. Then ask Codex to use:

```text
Use $blueprint-driven-project-runner to create a blueprint for this project before execution.
```

## Add Governance Files To A Project

After installing the skill, run:

```bash
python ~/.codex/skills/blueprint-driven-project-runner/scripts/install_governance_system.py --project /path/to/project --module "Your Module"
```

Windows PowerShell example:

```powershell
python "$env:USERPROFILE\.codex\skills\blueprint-driven-project-runner\scripts\install_governance_system.py" --project "C:\path\to\project" --module "Your Module"
```

This creates a lightweight control system inside the target project:

```text
docs/ai-control/
tools/ai-control/
```

## Common Commands

Lint blueprint records:

```bash
python tools/ai-control/lint_blueprints.py --project .
```

Generate a goal prompt from ready blueprint records:

```bash
python tools/ai-control/generate_goal_prompt.py --project . --module "Inventory" --record INVENTORY-IMPORT-IDEMPOTENCY-001 --work-slice WS-IMPORT-001
```

Lint generated goal prompts:

```bash
python tools/ai-control/lint_goal_prompt.py --project .
```

Show project status:

```bash
python tools/ai-control/status.py --project .
```

Generate a fresh-thread handoff package:

```bash
python tools/ai-control/generate_handoff_package.py --project . --module "Inventory" --record INVENTORY-IMPORT-IDEMPOTENCY-001 --work-slice WS-IMPORT-001
```

## Minimal Workflow

1. Install the governance system into your project.
2. Fill in executable blueprint records until each important requirement has stable inputs, behavior, acceptance, and verification.
3. Run `lint_blueprints.py`.
4. Generate a bounded goal prompt for one work slice.
5. Run `lint_goal_prompt.py`.
6. Execute only that goal prompt.
7. Report evidence against the blueprint records.
8. Use `generate_handoff_package.py` when moving work to a fresh thread.

## Validation

Validate the skill folder:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/blueprint-driven-project-runner
```

Compile bundled scripts:

```bash
python -m py_compile scripts/*.py
```

## Design Principle

The first principle is simple:

> Complete the referenced executable blueprint records exactly, with evidence, without expanding scope.

The skill is intentionally narrow. It does not try to replace product thinking, design judgment, engineering review, or user approval. It gives AI-assisted projects a stable control surface so large work can be planned, executed, reviewed, and resumed with less drift.

## License

MIT
