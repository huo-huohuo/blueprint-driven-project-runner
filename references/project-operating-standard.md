# Blueprint Governance Operating Standard

This is the durable project-level standard for large AI-assisted work. Install it into a target repository as `docs/ai-control/00-operating-standard.md` and reference it from `AGENTS.md`.

## Authority

For AI-assisted project work, use this source order:

1. Current user instruction.
2. `AGENTS.md`.
3. `docs/ai-control/00-operating-standard.md`.
4. `docs/ai-control/00-control-index.md`.
5. Module blueprint files and execution task ledger.
6. Current code, tests, schemas, routes, and runtime commands.
7. Chat history.

Chat history cannot override committed project rules unless the user explicitly says so.

## Core Rule

No executable blueprint, no execution task ledger, no long-running implementation.

Summary briefs, PRD paragraphs, vague plans, and feature lists do not authorize coding. Broad work requires ready executable blueprint records, execution ledger rows, and an execution contract.

Technical areas require user-checkable previews. For backend, data, integration, automation, infrastructure, or background work, use a questionnaire first, then compile technical records.

After blueprints are ready, decompose them into the execution ledger, then generate a goal prompt before long-running execution. The goal prompt must make blueprint and ledger completion the first principle.

## Required Project Files

Minimum files:

```text
AGENTS.md
docs/ai-control/00-operating-standard.md
docs/ai-control/00-control-index.md
docs/ai-control/01-run-card.md
docs/ai-control/90-maturity-dashboard.md
docs/ai-control/91-execution-ledger.md
docs/ai-control/92-drift-log.md
tools/ai-control/lint_blueprints.py
tools/ai-control/generate_goal_prompt.py
tools/ai-control/lint_goal_prompt.py
tools/ai-control/generate_handoff_package.py
tools/ai-control/status.py
```

Per module:

```text
docs/ai-control/<module>/product-blueprint.md
docs/ai-control/<module>/interface-blueprint.md
docs/ai-control/<module>/engineering-blueprint.md
docs/ai-control/<module>/acceptance-blueprint.md
docs/ai-control/<module>/work-slices.md
```

## Executable Blueprint Record

Every executable record must include:

```text
ID:
Type: product / interface / engineering / data / integration / automation / infrastructure / acceptance / safety / ops
Source:
Current Evidence:
Target Behavior:
Forbidden Result:
Preview:
Acceptance:
Verification:
Owner:
Status: draft / needs-decision / ready / accepted / deprecated
Confidence: low / medium / high
Open Questions:
```

Only `ready` or `accepted` records can authorize Execution mode.

## Execution Ledger

Long-running execution must be decomposed into `docs/ai-control/91-execution-ledger.md` before implementation.

The ledger is the execution queue. It must include row-level goals, completion paths, acceptance standards, verification methods, evidence, status, accepted/not accepted, blocker or skip reason, and resume condition.

Required statuses:

```text
planned / active / blocked / shelved / skipped / verified / accepted
```

Work one row at a time. Verify a row before marking it `verified`; mark it `accepted` only when the acceptance condition is satisfied. If a row is blocked by missing information, missing access, or high-risk confirmation, mark it `blocked` or `shelved` with a resume condition and continue to the next independent row.

## Definition Of Ready

A record is ready only when:

- all required fields exist
- `Source` cites where the requirement came from
- `Current Evidence` describes current behavior or says `NOT_CHECKED`
- `Target Behavior` is observable
- `Forbidden Result` blocks known wrong directions
- `Preview` lets a non-specialist inspect the intended behavior before implementation
- `Acceptance` can pass or fail
- `Verification` names a method
- no required field says `DECISION_NEEDED`
- status is `ready` or `accepted`

## Technical Blueprint Rule

For technical work, the user confirms business facts; the agent compiles technical contracts.

Ask for only the facts needed:

- outcome
- actor
- trigger
- before state
- action
- after state
- forbidden outcomes
- repeated-action behavior
- failure behavior
- boundaries
- evidence
- risk

Then produce a preview checklist:

- business flow
- before/after example
- inputs and outputs
- state rules
- boundaries
- failure matrix
- evidence plan

## Required Modes

- **Install**: create or refresh governance files; no product code changes.
- **Blueprint Compiler**: convert intent into executable records; no product code changes.
- **Blueprint Audit**: check records for readiness; no product code changes.
- **Ledger Compiler**: decompose ready or near-ready records into execution ledger rows; no product code changes.
- **Goal Prompt**: generate a target/goal prompt from ready blueprint records; no product code changes.
- **Status**: summarize project progress and blockers; no product code changes.
- **Handoff**: generate a fresh-thread package from ready records; no product code changes.
- **Execution**: implement ready records under an execution contract.
- **Recovery**: stop drift, classify changes, and restore control.
- **Coordination**: split work across threads and manage ownership.

## Goal Prompt Rule

A long-running or target-mode execution must start from a goal prompt derived from ready blueprint records.

Required goal prompt sections:

- project root and module
- first principle: complete referenced blueprints exactly, with evidence
- governing docs to read first
- blueprint record IDs
- work slice ID
- execution ledger file and row IDs
- allowed changes
- forbidden changes
- data policy
- verification plan
- evidence required
- stop conditions
- unexpected discovery rule

Forbidden goal prompt language:

- improve generally
- continue optimizing
- fix anything you notice
- make the whole module mature
- refactor as needed

If the prompt cannot cite ready blueprint records, return to Blueprint Compiler or Blueprint Audit mode.

Before starting from a generated prompt, lint it:

```bash
python tools/ai-control/lint_goal_prompt.py --project .
```

## Status And Handoff

Use status before starting or resuming long-running work:

```bash
python tools/ai-control/status.py --project .
```

Use a handoff package for new module threads:

```bash
python tools/ai-control/generate_handoff_package.py --project . --module "<module>" --record "<record-id>" --work-slice "<slice-id>"
```

A handoff package must include activation prompt, goal prompt, blueprint records, verification plan, and handoff summary.

## Execution Contract

Every implementation run must define:

```text
Contract ID:
Date:
Blueprint Record IDs:
Work Slice IDs:
Execution Ledger Row IDs:
Objective:
Allowed Changes:
Forbidden Changes:
Data Policy:
Verification Plan:
Evidence Required:
Stop Condition:
```

If a required change falls outside the contract, stop and report.

## Evidence Rules

Completion requires evidence. Prefer stronger evidence:

1. source inspection
2. syntax/type/lint check
3. unit/golden test
4. integration/API check
5. browser screenshot or UI flow
6. representative real-data validation
7. user acceptance

Do not report "complete" when only weak evidence was collected.

## High-Risk Actions

Require explicit user confirmation before:

- external side effects
- production-like data writes
- data deletion
- schema or migration changes
- access-control changes
- deployment changes
- background job cursor or offset mutation
- bulk automated actions

Ordinary in-scope reads, local edits, local tests, local build checks, local evidence files, and updates to allowed docs/control artifacts are covered by the execution contract. Do not ask for granular permission for those steps. If high-risk confirmation is needed but independent ledger rows remain, shelve the blocked row and keep moving.

## Drift Recovery

When progress becomes unclear:

1. Freeze implementation.
2. Check git status.
3. Classify changed files as contracted, supporting, useful-uncontracted, suspicious, or unrelated.
4. Identify the missing gate: blueprint, lint, contract, scope, or evidence.
5. Propose containment.
6. Update the drift log.

Never use destructive reset commands unless the user explicitly asks.

## Multi-Thread Rule

Use one control thread for standards, blueprints, sequencing, and integration. Use module threads for bounded work. High-conflict files must have one owner at a time.

Module thread prompts must include:

- project root
- module scope
- blueprint record IDs
- allowed files
- forbidden files
- verification plan
- stop condition

## Preflight Command

Before broad implementation:

```bash
python tools/ai-control/lint_blueprints.py --project .
python tools/ai-control/generate_goal_prompt.py --project . --module "<module>" --record "<record-id>"
python tools/ai-control/lint_goal_prompt.py --project .
python tools/ai-control/status.py --project .
```

If the linter reports errors, do not enter Execution mode.
