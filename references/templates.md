# Blueprint-Driven Project Templates

Use these templates to create project truth that future agents can execute against. A document may start with a short discovery brief, but only executable blueprint records authorize implementation.

## 1. Executable Blueprint Record

````markdown
### <MODULE>-<AREA>-001 <short title>

ID: <MODULE>-<AREA>-001
Type: product / interface / engineering / data / integration / automation / infrastructure / acceptance / safety / ops
Source:
- DECISION_NEEDED
Current Evidence:
- NOT_CHECKED
Target Behavior:
- DECISION_NEEDED
Forbidden Result:
- DECISION_NEEDED
Preview:
- DECISION_NEEDED
Acceptance:
- DECISION_NEEDED
Verification:
- DECISION_NEEDED
Owner: DECISION_NEEDED
Status: draft
Confidence: low
Open Questions:
- DECISION_NEEDED
````

## 2. Project Control Index

````markdown
# AI Project Control Index

This project uses blueprint-bound AI execution. Broad implementation must cite executable blueprint records, execution ledger rows, allowed scope, forbidden scope, and acceptance evidence.

## Project Root

`<absolute path>`

## Control Rule

No executable blueprint, no execution ledger, no long-running implementation. Summary briefs cannot authorize coding.

## Modules

| Module | Owner Thread | Scope | Forbidden Scope | Status |
| --- | --- | --- | --- | --- |
| Core Product | | | | planned |

## High-Conflict Areas

| Area | Current Owner | Rule |
| --- | --- | --- |
| app/router entrypoints | | serialize changes |
| shared database schema | | confirm before migration |
| access-control code | | owner only |
| background workers/cursors | | no cursor or offset mutation without approval |
| external side effects or production-like writes | | explicit human confirmation |

## Current Priority

| Date | Priority | Contract | Status |
| --- | --- | --- | --- |
| | | | |
````

## 3. Run Card

````markdown
# Run Card

## Mode

Intake / Blueprint Compiler / Blueprint Audit / Ledger Compiler / Goal Prompt / Execution / Recovery / Coordination

## User Outcome

## Project Facts Read

- 

## Discovery Brief

Short source-aware understanding. This section cannot authorize coding.

## Blocking Unknowns

- 

## Next Artifact

Executable blueprint records / work slice / execution ledger / execution contract / evidence report / recovery plan
````

## 4. Product Blueprint

````markdown
# Product Blueprint: <module>

## Discovery Brief

Short context only. Do not use this section as an implementation contract.

## Users

| User | Daily Job | Pain | Success Signal |
| --- | --- | --- | --- |
| | | | |

## Scope

Owns:
- 

Does not own:
- 

## Executable Blueprint Records

### <MODULE>-PRODUCT-001 <short title>

ID: <MODULE>-PRODUCT-001
Type: product
Source:
- DECISION_NEEDED
Current Evidence:
- NOT_CHECKED
Target Behavior:
- DECISION_NEEDED
Forbidden Result:
- DECISION_NEEDED
Preview:
- workflow checklist:
- user journey:
- no-go list:
Acceptance:
- DECISION_NEEDED
Verification:
- DECISION_NEEDED
Owner: DECISION_NEEDED
Status: draft
Confidence: low
Open Questions:
- DECISION_NEEDED
````

## 5. Interface Blueprint

````markdown
# Interface Blueprint: <module or page id>

## Discovery Brief

Short context only. Do not use this section as an implementation contract.

## Executable Blueprint Records

### <MODULE>-INTERFACE-001 <screen/state>

ID: <MODULE>-INTERFACE-001
Type: interface
Source:
- DECISION_NEEDED
Current Evidence:
- NOT_CHECKED
Target Behavior:
- Initial state:
- Loading state:
- Empty state:
- Selected state:
- Error state:
Forbidden Result:
- DECISION_NEEDED
Preview:
- target screenshot / wire preview / static preview / state checklist / DECISION_NEEDED
Acceptance:
- DECISION_NEEDED
Verification:
- browser screenshot / Playwright screenshot / manual screenshot / DECISION_NEEDED
Owner: DECISION_NEEDED
Status: draft
Confidence: low
Open Questions:
- DECISION_NEEDED

## References

- screenshot/prototype:
- comparable product:
- notes:
````

## 6. Engineering Blueprint

````markdown
# Engineering Blueprint: <module>

## Discovery Brief

Short context only. Do not use this section as an implementation contract.

## Executable Blueprint Records

### <MODULE>-ENGINEERING-001 <contract>

ID: <MODULE>-ENGINEERING-001
Type: engineering
Source:
- DECISION_NEEDED
Current Evidence:
- NOT_CHECKED
Target Behavior:
- Business Scenario:
- Actor:
- Trigger:
- Before State:
- Action:
- After State:
- System Boundary:
- Data Contract:
- Operation Contract:
- Access Rule:
- Repeat/Idempotency Rule:
- Failure Behavior:
- Observability:
Forbidden Result:
- DECISION_NEEDED
Preview:
- business flow checklist:
- before/after example:
- input/output sample:
- state rules:
- boundaries:
- failure matrix:
- evidence plan:
Acceptance:
- DECISION_NEEDED
Verification:
- unit test / API check / log check / DECISION_NEEDED
Owner: DECISION_NEEDED
Status: draft
Confidence: low
Open Questions:
- DECISION_NEEDED

## Data Write Policy

- Read-only:
- Local/cache writes:
- Production-like writes:
- Requires explicit confirmation:
````

## 7. Acceptance Blueprint

````markdown
# Acceptance Blueprint: <module>

## Executable Blueprint Records

### <MODULE>-ACCEPTANCE-001 <golden case>

ID: <MODULE>-ACCEPTANCE-001
Type: acceptance
Source:
- DECISION_NEEDED
Current Evidence:
- NOT_CHECKED
Target Behavior:
- Given:
- When:
- Then:
Forbidden Result:
- DECISION_NEEDED
Preview:
- golden case checklist:
- pass/fail table:
Acceptance:
- DECISION_NEEDED
Verification:
- unit/golden test / browser flow / API check / manual check / DECISION_NEEDED
Owner: DECISION_NEEDED
Status: draft
Confidence: low
Open Questions:
- DECISION_NEEDED

## Completion Criteria

- 

## Stop Criteria

Stop and report if:
- 
````

## 8. Work Slices

````markdown
# Work Slices: <module>

| ID | Blueprint Records | Problem | Outcome | Appetite | Hill Position | Owner | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WS-001 | | | | | raw | | |

## Slice Detail: WS-001

Blueprint Records:
- 
Problem:
User-visible Outcome:
Appetite:
Owned Files:
Forbidden Files:
Golden Cases:
No-gos:
Evidence:
````

## 9. Goal Prompt

````markdown
# Goal Prompt: <module> / <work slice>

Use $blueprint-driven-project-runner.

## Project

Project root:
Module:
Mode: Execution

## First Principle

Complete the referenced executable blueprint records exactly, with evidence. Do not optimize beyond the records, invent adjacent work, or rewrite unrelated areas.

## Read First

- AGENTS.md
- docs/ai-control/00-operating-standard.md
- docs/ai-control/00-control-index.md
- relevant module blueprint files
- relevant work-slices.md
- docs/ai-control/91-execution-ledger.md
- current git status

## Blueprint Records

- 

## Work Slice

ID:
Outcome:
Appetite:

## Execution Ledger

Ledger file: docs/ai-control/91-execution-ledger.md
Rows:
- TODO

## Allowed Changes

- 

## Forbidden Changes

- 

## Data Policy

- 

## Verification Plan

- 

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
````

## 10. Execution Contract

````markdown
# Execution Contract: <id>

## Date

YYYY-MM-DD

## Mode

Execution

## Blueprint Record IDs

- 

## Work Slice IDs

- 

## Execution Ledger Row IDs

- TODO

## Objective

## Allowed Changes

- 

## Forbidden Changes

- 

## Data Policy

## Verification Plan

| Evidence | Method | Required |
| --- | --- | --- |
| | | |

## Stop Condition

## Final Report Required

- blueprint record ids addressed
- execution ledger rows accepted, blocked, shelved, or skipped
- files changed
- evidence collected
- golden cases pass/fail
- maturity movement
- risks
- rollback path
````

## 11. Handoff Package

````markdown
# Handoff Package: <module> / <work slice>

## Activation Prompt

Use $blueprint-driven-project-runner.

Project root:
Module:
Mode: Execution

Read this handoff package first:
- handoff-summary.md
- goal-prompt.md
- blueprint-records.md
- verification-plan.md

Do not rely on chat history. Complete only the referenced executable blueprint records with evidence.

## Required Files

- activation-prompt.md
- handoff-summary.md
- goal-prompt.md
- blueprint-records.md
- verification-plan.md
````

## 12. Maturity Dashboard

````markdown
# Maturity Dashboard

| Module | Product Records | Interface Records | Engineering Records | Acceptance Records | Implementation | Real Data | Safety | Ops | Acceptance | Hill |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Core Product | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | raw |

Scoring:
- 0: absent
- 25: drafted
- 50: structurally complete
- 75: ready or accepted with representative evidence
- 100: accepted with regression protection
````

## 13. Execution Ledger

````markdown
# Execution Ledger

This is the execution queue. Complete one row at a time, verify it, then update the row before moving on.

## Task Queue

| ID | Blueprint Records | Work Slice | Goal | Completion Path | Scope / Files | Acceptance Standard | Verification Method | Evidence | Status | Accepted? | Blocker / Skip Reason | Resume Condition | Updated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LEDGER-001 | | | | | | | | | planned | no | | | |

Status values: planned / active / blocked / shelved / skipped / verified / accepted

## Run History

| Date | Contract ID | Ledger Rows | Files Changed | Evidence | Result | Next |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |
````

## 14. Drift Log

````markdown
# Drift Log

Use this when AI work changes too much, loops without visible improvement, or violates an executable blueprint record.

| Date | Symptom | Root Cause | Files Involved | Prevention Rule | Status |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
````

## 15. Decision Record

````markdown
# Decision Record: ADR-000 <title>

## Status

Proposed / Accepted / Superseded

## Context

What forces, constraints, or tradeoffs led to this decision?

## Decision

What will the project do?

## Consequences

Positive:
- 

Negative:
- 

Neutral:
- 

## Supersedes / Superseded By

- 
````
