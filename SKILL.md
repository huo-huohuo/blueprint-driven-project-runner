---
name: blueprint-driven-project-runner
description: Use when Codex is asked to plan, run, continue, audit, recover, or coordinate a large or long-running AI-assisted project; when goals are vague, progress is unclear, previous runs changed too many places, or the user wants executable blueprints, spec-driven development, acceptance standards, golden cases, execution contracts, maturity dashboards, multi-thread coordination, or less hands-on supervision. Also use before broad refactors, product builds, backend rewrites, high-risk automation, or public project governance.
---

# Blueprint-Driven Project Runner

## Mission

Launch the Blueprint Governance System for large AI-assisted projects. The skill is the entry point; the durable project standard lives in the target repository; scripts enforce the standard.

Large AI projects fail when the prompt expresses desire but not the judging system. This skill creates and enforces that judging system before implementation.

The loop is:

```text
intent -> questionnaire -> discovery brief -> executable blueprint records -> preview checklist -> work slices -> goal prompt -> execution contract -> implementation -> evidence -> ledger
```

## Layer Model

Use three layers:

- **Launcher skill**: this folder. It teaches Codex how to install, read, and enforce the system.
- **Project operating standard**: `AGENTS.md` plus `docs/ai-control/` in the target repo. This is the durable project constitution.
- **Enforcement scripts**: project-local lint/preflight tools such as `tools/ai-control/lint_blueprints.py`.

Do not rely on chat history as the project constitution. For any serious project, install or update the project operating standard first.

## Non-Negotiable

No executable blueprint, no implementation.

A paragraph summary is not a blueprint. A plan is not a blueprint. A PRD-style description is not a blueprint. Only an executable blueprint record can authorize broad implementation.

Emergency bug fixes are allowed, but keep them narrow and record the blueprint gap that allowed the bug.

## Discovery Brief vs Executable Blueprint

Use different names for different artifacts:

- **Discovery brief**: source-aware understanding, useful for discussion, cannot authorize coding.
- **Executable blueprint record**: atomic construction constraint with source, target behavior, forbidden result, preview, acceptance, and verification.
- **Preview**: a user-readable representation of the blueprint before implementation. Frontend previews may be visual; technical/backend previews should usually be checklists, state tables, before/after examples, and failure matrices.
- **Work slice**: bounded implementation unit derived from one or more executable blueprint records.
- **Goal prompt**: a handoff prompt generated from ready blueprints and work slices. It constrains goal-mode execution to completing the blueprint, not inventing a new direction.
- **Execution contract**: per-run permission slip that names allowed files, forbidden files, data policy, and evidence.

If the user asks for "blueprint", produce executable blueprint records unless they explicitly ask for a summary.

## Required Blueprint Record

Every executable blueprint record must use this shape:

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

Rules:

- `ID` must be stable and specific, such as `MODULE-FLOW-INITIAL-001`.
- `Source` must name where the requirement came from: user instruction, project doc, code evidence, screenshot, issue, or inference.
- `Current Evidence` must cite current behavior or say `NOT_CHECKED`.
- `Target Behavior` must contain observable behavior, not adjectives.
- `Forbidden Result` must say what future agents must not do.
- `Preview` must show how a human can review the intended behavior before implementation.
- `Acceptance` must define pass/fail criteria.
- `Verification` must name the method: test, screenshot, browser flow, API check, log check, manual check, or `DECISION_NEEDED`.
- Unknown required information must be written as `DECISION_NEEDED`, not filled with vague prose.

## Blueprint Definition Of Ready

A record is not ready for execution unless all are true:

- It has all required fields.
- It has a stable ID.
- It has at least one source.
- It has target behavior with observable nouns and verbs.
- It has at least one forbidden result.
- It has a preview that a non-specialist can inspect.
- It has acceptance criteria that can pass or fail.
- It has a verification method.
- It does not depend on chat memory to be understood.
- It does not use vague words as a substitute for criteria.
- Its status is `ready` or `accepted`.

If any item fails, keep the record as `draft` or `needs-decision` and do not enter Execution mode.

## What Does Not Count

Reject these as blueprint substitutes:

- pure paragraphs
- "we need to optimize/improve/make mature" statements
- feature lists without forbidden results
- UI descriptions without states
- technical descriptions without user-checkable scenarios or preview checklists
- acceptance criteria such as "works correctly" or "looks good"
- summaries that contain no source, no evidence, and no verification

When an agent produces these, label the output `Discovery brief only` and compile executable records next.

## Source Hierarchy

Build facts in this order:

1. Current user instruction.
2. Project rules such as `AGENTS.md`, `.codex/`, governance docs, or repo-specific rules.
3. Existing `docs/ai-control/` artifacts, specs, ADRs, issue docs, PRDs, test plans, and task ledgers.
4. Current code, tests, routes, schemas, services, and runtime commands.
5. Git state and changed files.
6. Recent chat history or thread summaries.
7. External references, only when the user asks or the domain is unstable.

If sources conflict, state the conflict and choose the source closest to current project truth. Do not silently merge contradictions.

## Operating Modes

Start each substantial response by choosing one mode and one sentence of rationale.

- **Intake mode**: identify outcome, module boundary, appetite, no-gos, and missing facts.
- **Install mode**: install or refresh the project-level governance standard. Do not change product code.
- **Blueprint Compiler mode**: turn discovery material into executable blueprint records. Do not change product code.
- **Blueprint Audit mode**: lint existing blueprints for readiness and vagueness. Do not change product code.
- **Goal Prompt mode**: generate a target/goal prompt from ready blueprint records and work slices. Do not change product code.
- **Status mode**: summarize project progress, blockers, ready records, goal prompts, and executing slices. Do not change product code.
- **Handoff mode**: generate a fresh-thread handoff package from ready records. Do not change product code.
- **Execution mode**: implement one or a few ready records under an execution contract.
- **Recovery mode**: stop drift, classify changes, restore control, and record prevention rules.
- **Coordination mode**: split work across independent threads, assign owners, and serialize high-conflict files.

## Gates

Use gates to prevent long-run drift.

### 0. Installation Gate

For a large project, first check whether project-level rules exist:

- `AGENTS.md`
- `docs/ai-control/00-operating-standard.md`
- `docs/ai-control/00-control-index.md`
- `docs/ai-control/90-maturity-dashboard.md`
- project-local blueprint linter such as `tools/ai-control/lint_blueprints.py`

If missing and the user asked to set up governance, run:

```bash
python scripts/install_governance_system.py --project <project-root> --module "<module name>"
```

If the project already has governance docs, read them and extend them instead of replacing them.

### 1. Intent Gate

Before shaping work, identify:

- user outcome
- target users/workflows
- module boundary
- current pain or failure mode
- appetite: time, risk, or scope limit
- no-gos

If any item is unknowable from source, infer conservatively and label the inference, or ask only the blocking question.

### 2. Blueprint Gate

Broad work is allowed only when executable records exist for the relevant layers:

- product: users, scope, workflows, pages, non-goals
- interface: layout, states, actions, empty/error/loading behavior, target references
- engineering: data objects, APIs, services, permissions, idempotency, failure behavior, data-write policy
- acceptance: golden cases, tests, screenshots, manual checks, completion criteria, stop criteria
- safety/ops: high-risk actions, logs, rollback, irreversible actions, production-like write policy

Do not call a document a blueprint if it is only a summary. Compile records.

### 3. Lint Gate

Before Execution mode, inspect or run a blueprint readiness check:

```bash
python scripts/lint_blueprints.py --project <project-root>
```

If the linter is unavailable, manually apply the Blueprint Definition Of Ready. Treat failures as blockers, not suggestions.

### 4. Goal Prompt Gate

After blueprints are ready and before a long-running goal starts, generate a goal prompt that makes blueprint fulfillment the first principle.

A goal prompt must include:

- project root
- module
- governing docs to read first
- blueprint record ids
- work slice ids
- first principle: complete the referenced blueprints exactly
- allowed files/directories
- forbidden files/directories
- data policy
- verification plan
- evidence required
- stop conditions
- rule for unexpected discoveries: record backlog/drift, do not implement outside scope

Do not generate a goal prompt from draft, needs-decision, contradictory, or unlinted records.

Use:

```bash
python scripts/generate_goal_prompt.py --project <project-root> --module "<module>" --record <RECORD-ID>
```

If the project has a local copy, prefer:

```bash
python tools/ai-control/generate_goal_prompt.py --project . --module "<module>" --record <RECORD-ID>
```

### 5. Contract Gate

Every execution run needs:

- contract id and date
- mode
- blueprint record ids and work slice ids
- objective
- allowed files/directories
- forbidden files/directories
- data-write policy
- verification plan
- evidence required in final response
- stop condition

If a necessary change touches forbidden scope, stop and report. Do not expand the contract silently.

### 6. Evidence Gate

Completion requires evidence. Choose the strongest feasible evidence:

1. static inspection only
2. syntax/type checks
3. unit/golden tests
4. integration/API checks
5. browser screenshots or UI flow checks
6. representative real-data validation
7. user acceptance

Report gaps honestly. Do not claim maturity from activity or file count.

## Blueprint Compiler Workflow

When asked to "make a blueprint":

1. Read source facts.
2. If the area is technical or backend-heavy, ask or fill the technical questionnaire before writing technical contracts.
3. Output a short discovery brief only if useful.
4. Compile atomic executable records.
5. Add a preview for each record: visual preview for UI, checklist/state/sample preview for technical work.
6. Mark missing fields as `DECISION_NEEDED`.
7. Add records to the relevant blueprint files if the user asked for project artifacts.
8. Create work slices from ready or near-ready records.
9. Produce a decision queue for records that are not ready.
10. If records are ready and the user wants execution, generate a goal prompt instead of starting broad work directly.
11. Stop before implementation unless the user explicitly approves Execution mode.

The main output should be records, not prose.

## Goal Prompt Protocol

Use Goal Prompt mode when the blueprint is ready and the user wants target-mode or long-running execution.

First principle:

```text
The goal is to complete the referenced executable blueprint records exactly, with evidence. Do not optimize beyond the records, invent adjacent work, or rewrite unrelated areas.
```

Required behavior:

1. Read the project operating standard.
2. Confirm the blueprint records are `ready` or `accepted`.
3. Run or manually apply blueprint lint.
4. Generate the goal prompt from records and work slices.
5. Include the exact stop condition.
6. Include how progress will be reported against the blueprint.
7. Do not weaken the prompt with broad language such as "improve as much as possible".

The goal prompt is not a brainstorming prompt. It is a controlled execution brief.

## Status And Handoff

Use Status mode before starting, resuming, or coordinating a large project:

```bash
python tools/ai-control/status.py --project .
```

Use Handoff mode when starting a fresh module thread:

```bash
python tools/ai-control/generate_handoff_package.py --project . --module "<module>" --record "<record-id>" --work-slice "<slice-id>"
```

Before starting from a goal prompt, lint it:

```bash
python tools/ai-control/lint_goal_prompt.py --project .
```

A handoff package must include activation prompt, goal prompt, blueprint records, verification plan, and handoff summary.

## Technical Blueprint Questionnaire

For backend, data, integration, automation, infrastructure, or other technical areas, do not ask non-technical users to design APIs, schemas, or internal services directly.

Use the questionnaire in `references/technical-blueprint-questionnaire.md`:

1. Ask the user for business-understandable facts: actor, trigger, before state, action, after state, forbidden outcomes, risk level, and proof of completion.
2. Infer the technical draft from project source when possible.
3. Separate user-confirmable facts from AI-compiled technical details.
4. Mark unclear technical decisions as `DECISION_NEEDED`.
5. Present the technical preview as checklists and examples before asking for approval.

The user confirms the scenario and risks; the agent compiles the technical contract.

## Preview Rule

Every executable record needs a `Preview`.

Use previews by record type:

- Product: workflow checklist, user journey, no-go list.
- Interface: target screenshot, wire/static preview, state list, or reference.
- Engineering/data/integration: business flow checklist, before/after data sample, input/output sample, state table, boundary list, failure matrix.
- Acceptance: golden case checklist.
- Safety/ops: risk-control checklist and rollback checklist.

For technical records, prefer clear tables and examples over architecture prose. A user should be able to say "yes, this is the behavior I want" without understanding the implementation internals.

## Install Workflow

When the user asks to apply this system to a project:

1. Inspect project root, existing `AGENTS.md`, `docs/`, `tools/`, and git state.
2. Install or refresh the project operating standard using the installer script.
3. Create missing `docs/ai-control/` artifacts.
4. Copy the linter into project-local tools unless the project already has an equivalent.
5. Copy the goal prompt generator into project-local tools unless the project already has an equivalent.
6. Copy status, goal-prompt lint, and handoff tools unless the project already has equivalents.
7. Do not modify product code.
8. Report installed files, skipped existing files, and the first command the user should run.

## Work Slice Standard

Each slice must fit this shape:

```text
ID:
Module:
Blueprint Records:
Problem:
User-visible Outcome:
Appetite:
Hill Position: raw / shaped / validated / executing / verified / accepted
Owned Files:
Forbidden Files:
Golden Cases:
Evidence:
No-gos:
```

Split the slice if it mixes unrelated UI/backend decisions, needs multiple owners, touches high-conflict files, cannot be verified in one pass, or has unknowns larger than the implementation.

## Execution Standard

During implementation:

- Read before editing.
- Keep changes inside the contract.
- Prefer small, reviewable edits.
- Put better new ideas into backlog or drift log.
- Update tests/golden cases when behavior changes.
- Record decisions that affect architecture or future agents.
- Treat migrations, external side effects, access-control changes, deployment changes, production-like writes, and destructive operations as high risk.

## Acceptance Standards

Use golden cases for behavior that agents often break:

- identity and deduplication
- classification and routing
- suppression, approval, and safety logic
- real evidence versus simulated or draft evidence
- access and visibility rules
- state transitions
- frontend navigation and layout states
- data import/export boundaries

For scenario-like behavior, write:

```text
Given:
When:
Then:
Forbidden:
Evidence:
```

For frontend work, require a target reference, textual layout contract, or approved prototype before broad implementation. Verify with screenshots or browser checks when possible. Report target versus actual.

For technical/backend work, start from the questionnaire, then compile data objects, operations, contracts, access rules, idempotency, audit/log fields, failure behavior, migration policy, and tests. Show the checklist preview before broad implementation.

## Progress Model

Measure movement by reduced uncertainty and accepted evidence.

Hill positions:

- **raw**: goal exists but shape is unclear
- **shaped**: problem, appetite, no-gos, and target outcome are written
- **validated**: approach and key unknowns have been checked
- **executing**: implementation is underway inside a contract
- **verified**: evidence passed, user acceptance may still be pending
- **accepted**: user or project standard accepts the result

Maturity scoring:

```text
0: absent
25: drafted
50: usable
75: validated on representative evidence
100: accepted with regression protection
```

A module with polished code but no acceptance evidence is not mature.

## Multi-Thread Projects

For independent Codex threads:

- Keep one control thread for executable blueprints, sequencing, ownership, and integration.
- Give each module thread a compact activation prompt, project root, module scope, allowed files, forbidden files, and current contract.
- Do not fork huge historical threads when a fresh thread can rebuild from project docs.
- Serialize high-conflict files to one owner.
- Use handoff requests instead of cross-module edits.
- Keep the execution ledger as shared memory, not the chat transcript.

High-conflict areas commonly include main app/router files, shared schemas, access-control code, startup scripts, background workers, migration scripts, external side effects, and production-like data paths.

## Recovery Rules

Use Recovery mode when work feels circular, progress is invisible, or the user reports that AI changed wrong areas.

1. Freeze new implementation.
2. Capture git status and changed files.
3. Classify changes as contracted, supporting, useful-uncontracted, suspicious, or unrelated.
4. Identify the missing blueprint, contract, lint, or evidence gate.
5. Propose containment: keep, revert manually, split, or move to backlog.
6. Record a prevention rule in the drift log.

Do not use destructive reset commands unless the user explicitly asks.

## Stop Conditions

Stop and report when:

- records are missing, contradictory, or too vague
- required records are not `ready` or `accepted`
- contract is absent for broad work
- required change exceeds allowed scope
- high-risk action lacks explicit confirmation
- verification cannot be run
- runtime directory differs from edited directory
- unrelated worktree changes may be overwritten
- the contracted slice is complete

## Resources

- Read `references/project-operating-standard.md` when installing or explaining the higher-level project standard.
- Read `references/templates.md` when creating or updating control artifacts.
- Read `references/technical-blueprint-questionnaire.md` when compiling backend, data, integration, automation, infrastructure, or other technical blueprints.
- Read `references/quality-bars.md` when auditing readiness or recovering from drift.
- Read `references/blueprint-examples.md` when the user reports vague blueprints or asks for examples.
- Read `references/goal-prompt-protocol.md` when generating target/goal prompts after blueprints are ready.
- Use `scripts/install_governance_system.py` to install the full project-level governance system.
- Use `scripts/scaffold_control_pack.py` to create a starter `docs/ai-control/` pack.
- Use `scripts/lint_blueprints.py` before execution or when blueprints seem summary-like.
- Use `scripts/generate_goal_prompt.py` to generate a goal-mode prompt from ready blueprint records.
- Use `scripts/lint_goal_prompt.py` before starting goal-mode execution.
- Use `scripts/status.py` to summarize project progress and blockers.
- Use `scripts/generate_handoff_package.py` to create fresh-thread handoff packages.
