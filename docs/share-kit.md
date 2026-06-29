# Share Kit

Use these snippets when introducing Blueprint-Driven Project Runner in developer communities.

## One-Line Pitch

Blueprint-Driven Project Runner stops long-running Codex projects from drifting by requiring executable blueprints, execution ledgers, scoped goal prompts, startup gates, and evidence before broad implementation.

## Short Post

I built a Codex plugin for a failure mode I kept hitting: long-running AI coding agents would work for hours or days, change many files, and still be unable to prove what actually improved.

The fix is to stop treating a prompt as the project contract.

Blueprint-Driven Project Runner forces large tasks through:

- executable blueprint records
- row-by-row execution ledgers
- target-mode startup gates
- scoped goal prompts
- evidence-based progress reports
- recovery and handoff packages for stale threads

Core rule:

```text
No executable blueprint, no execution ledger, no long-running implementation.
```

Repository:
https://github.com/huo-huohuo/blueprint-driven-project-runner

## Longer Post

Most AI coding failures in large projects are not caused by weak implementation. They start earlier: the agent is asked to "optimize", "finish", "make mature", or "continue improving" without a judging system.

Blueprint-Driven Project Runner is a Codex plugin that turns those vague goals into durable project control artifacts:

- blueprint records with source evidence, target behavior, forbidden results, preview, acceptance, and verification
- execution ledgers that break broad work into rows with status, evidence, blockers, skip reasons, and resume conditions
- goal prompts that bind a run to specific blueprint record IDs and ledger row IDs
- a target-mode startup gate that fails closed when required artifacts are missing
- recovery rules for runs that changed too many files or lost visible progress

The goal is not more planning theater. The goal is to make long-running AI work measurable, resumable, and reviewable.

Repository:
https://github.com/huo-huohuo/blueprint-driven-project-runner

## Suggested GitHub Topics

- codex
- codex-skill
- ai-agents
- ai-coding
- ai-coding-agents
- prompt-engineering
- spec-driven-development
- software-governance
- project-management
- agentic-workflows

## Best Audiences

- developers using Codex or AI coding agents on multi-hour tasks
- builders with large frontend/backend refactors
- teams that need handoffs between AI sessions
- people frustrated by agents that produce large diffs without accepted progress

## Good Opening Question

Have you had an AI coding agent run for hours, change a lot of files, and still fail to prove what actually improved?
