# Goal Prompt Protocol

Use this after executable blueprint records are ready and before long-running or target-mode execution starts.

## First Principle

The goal prompt exists to complete the blueprint, not to reinterpret it.

```text
Complete the referenced executable blueprint records exactly, with evidence. Do not optimize beyond the records, invent adjacent work, or rewrite unrelated areas.
```

## Preconditions

Do not generate a goal prompt unless:

- project operating standard exists or has been read
- referenced blueprint records are `ready` or `accepted`
- records contain no `DECISION_NEEDED`
- records have Preview, Acceptance, and Verification
- lint passes or manual readiness check is documented
- work slice is bounded

If preconditions fail, return to Blueprint Compiler or Blueprint Audit mode.

## Required Goal Prompt Sections

```markdown
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
- current git status

## Blueprint Records

- <ID>: <one-line target>

## Work Slice

ID:
Outcome:
Appetite:

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
- referenced blueprint records are implemented and verified
- a required change exceeds allowed scope
- blueprint contradiction is found
- verification cannot run
- high-risk action needs confirmation
- unrelated worktree changes may be overwritten

## Unexpected Discoveries

Record as backlog, drift log, or open question. Do not implement outside the referenced records.
```

## Anti-Patterns

Do not write goal prompts that say:

- improve the project generally
- continue optimizing until mature
- fix anything you notice
- make the whole module production-ready
- refactor as needed
- use your judgment to complete adjacent issues

Replace those phrases with record IDs, allowed files, forbidden files, and evidence.

## Progress Reporting

A goal run should report progress against the blueprint:

```text
Record ID:
Status: not started / in progress / blocked / verified
Evidence:
Remaining gap:
```

If progress cannot be tied to a record ID, it is not valid progress for this goal.
