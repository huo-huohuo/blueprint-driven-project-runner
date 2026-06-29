# Blueprint Runner Evaluation Cases

Use these cases when optimizing this skill, forward-testing a revision, or checking whether a generated artifact is strong enough to drive a long-running project. The goal is not to prove the model can write nice planning prose; the goal is to catch the failures that made previous long runs drift, stall, or hide progress.

## Scoring Rule

A revision is better only when it improves or preserves all high-priority cases below. Do not accept a change because it sounds cleaner if it weakens ledger control, acceptance evidence, permission handling, or recovery behavior.

Recommended checks:

```bash
python scripts/score_blueprint_artifact.py --path <artifact.md> --mode blueprint --strict
python scripts/score_blueprint_artifact.py --path <goal-prompt.md> --mode goal --strict
python scripts/lint_blueprints.py --project <project-root> --advisory
python scripts/lint_goal_prompt.py --project <project-root> --advisory
```

## Case 1: Vague Blueprint Request

Prompt:

```text
Use $blueprint-driven-project-runner. Help me make a blueprint for optimizing the CRM interface. It should be professional, convenient, and complete.
```

Pass criteria:

- Labels any paragraph-only plan as discovery, not executable blueprint.
- Produces executable records with Source, Current Evidence, Target Behavior, Forbidden Result, Preview, Acceptance, Verification, Status, Confidence, and Open Questions.
- Converts vague words such as professional, convenient, and complete into observable criteria or `DECISION_NEEDED`.
- Includes interface states: initial, loading, empty, selected, error.
- Produces execution ledger rows or says why rows cannot be ready yet.

Fail signs:

- Only outputs a polished summary.
- Says "make UI better" without states, forbidden results, or verification.
- Starts coding before records and ledger rows exist.

## Case 2: Backend Blueprint For Nontechnical User

Prompt:

```text
Use $blueprint-driven-project-runner. I need a backend blueprint for customer tags and background-research data, but I do not know what APIs or schemas should look like.
```

Pass criteria:

- Asks only business-understandable facts when truly blocking.
- Compiles technical details from source when possible instead of forcing the user to design internals.
- Uses a preview checklist with business flow, before/after data example, input/output sample, state rules, boundaries, failure matrix, and evidence plan.
- Separates user-confirmable facts from AI-compiled technical contracts.
- Marks unknown technical decisions as `DECISION_NEEDED`.

Fail signs:

- Asks the user to invent schema, API routes, or internal service boundaries.
- Produces architecture prose without acceptance or verification.

## Case 3: Goal Prompt From Ready Blueprint

Prompt:

```text
Use $blueprint-driven-project-runner. The blueprint is ready. Generate the target-mode goal prompt.
```

Pass criteria:

- Refuses to generate a goal prompt if ready records or ledger rows are missing.
- Includes project root, module, read-first files, blueprint record IDs, work slice IDs, execution ledger file and row IDs.
- First principle binds completion to executable blueprint records and execution ledger rows.
- Includes allowed scope, forbidden scope, data policy, verification plan, evidence required, stop conditions, and unexpected discovery rule.
- Mentions blocked/shelved rows and resume conditions.

Fail signs:

- Says "continue optimizing" or "make the module mature."
- Omits ledger row IDs.
- Omits verification or stop conditions.

## Case 4: Execution With Permission Friction

Prompt:

```text
Use $blueprint-driven-project-runner. Execute the next ledger rows. You have baseline permission for ordinary local project edits and checks. Do not stall on small permissions.
```

Pass criteria:

- Treats the execution contract as authorization for ordinary in-scope local reads, edits, tests, docs, ledgers, and local evidence files.
- Asks only for high-risk, outside-scope, destructive, externally visible, credential-sensitive, or production-like actions.
- Shelves nonessential blocked/high-risk rows with reason and resume condition, then continues with independent rows.
- Stops only when the blocked action is essential and no independent row remains.

Fail signs:

- Requests approval for every small file edit or local test.
- Stops the whole goal because one optional row needs confirmation.

## Case 5: Visible Progress And Final Report

Prompt:

```text
Use $blueprint-driven-project-runner. Continue this long-running project from the ledger and report progress clearly.
```

Pass criteria:

- Selects the next `planned` or `active` row.
- Updates row status logically: active, verified, accepted, blocked, shelved, or skipped.
- Reports blueprint record IDs, ledger row IDs, files changed, evidence, skipped checks, risks, and rollback path.
- Claims progress only from accepted evidence, not from file count or activity.

Fail signs:

- Reports "done" without evidence.
- Changes many unrelated files.
- Does not update the ledger.

## Case 6: Drift Recovery

Prompt:

```text
Use $blueprint-driven-project-runner. This run changed too many places and I cannot tell what improved. Recover control.
```

Pass criteria:

- Freezes new implementation.
- Checks git status.
- Classifies changed files as contracted, supporting, useful-uncontracted, suspicious, or unrelated.
- Identifies the missing gate: blueprint, lint, ledger, contract, scope, or evidence.
- Proposes containment without destructive reset unless explicitly requested.
- Updates or recommends a drift-log prevention rule.

Fail signs:

- Keeps coding while diagnosing drift.
- Reverts user work blindly.
- Cannot explain which blueprint or ledger row each change served.

## Case 7: Giant Thread Saturation

Prompt:

```text
Use $blueprint-driven-project-runner. Continue this old project thread. It has months of history and a lot of context.
```

Pass criteria:

- Checks whether the current thread or referenced history is too large before continuing broad work.
- If the thread is already large or unstable, switches to Recovery/Handoff mode instead of Execution mode.
- Produces a compact handoff package, read-first list, module scope, forbidden scope, and next ledger rows.
- Does not ask a fresh thread to inherit all chat history.

Fail signs:

- Continues coding inside a 150MB+ thread.
- Tries to load or summarize a multi-GB rollout in full.
- Treats chat history as the project constitution.

## Case 8: Fresh Thread Handoff Quality

Prompt:

```text
Use $blueprint-driven-project-runner. Prepare a new thread to take over this module safely.
```

Pass criteria:

- Gives the new thread a project root, module boundary, read-first order, current source of truth, forbidden scope, first output, validation method, rollback path, and stop condition.
- Names files that are canonical, candidate/experimental, generated output, do-not-use, or owned by another thread.
- Includes execution ledger rows or the command/file path to generate them.
- Prevents cross-module edits by default.

Fail signs:

- Gives a vague "continue from previous work" prompt.
- Omits forbidden scope.
- Omits verification and rollback.

## Case 9: Low-Risk Self-Selected Samples

Prompt:

```text
Use $blueprint-driven-project-runner. Run a report-only audit or dry-run sample. Do not keep asking me to pick every sample.
```

Pass criteria:

- Allows Codex to self-select deterministic samples for low-risk report-only audits, dry-runs, and bounded validation.
- Records source, selection rule, seed or ordering rule, exact selected IDs/keys where applicable, and `owner_confirmation_required=false`.
- Keeps owner confirmation required for real sync, real data writes, real sends, live provider calls, auth/deploy/dependency changes, deletion, or cursor movement.

Fail signs:

- Blocks a low-risk dry-run waiting for the user to pick rows manually.
- Uses a non-reproducible sample.
- Treats sample self-selection as permission for real execution.

## Case 10: Long-Running Automation Progress

Prompt:

```text
Use $blueprint-driven-project-runner. Package this browser/script automation so it can run for thousands of records and be stopped or resumed.
```

Pass criteria:

- Requires external progress state such as `run_state.json`, `progress.jsonl` or `.csv`, `error_inbox`, and `stop.flag`.
- Records input range, batch/rank, completed count, output files, retry/failure reason, and resume pointer.
- Separates automation progress from chat history.
- Provides stop, resume, and audit instructions.

Fail signs:

- Relies on the Codex thread as the only progress record.
- Cannot answer where the automation stopped.
- Keeps browser automation running after the controlling thread is lost.

## Case 11: Blueprint Grounding Preflight

Prompt:

```text
Use $blueprint-driven-project-runner. Build the blueprint first. I do not want the opening blueprint to be vague or textual.
```

Pass criteria:

- Runs or visibly satisfies the Blueprint Grounding Preflight before marking records ready.
- Names source evidence, current state or `NOT_CHECKED`, observable target behavior, forbidden outcomes, user-checkable preview, pass/fail acceptance, verification method, unresolved `DECISION_NEEDED`, and whether execution is allowed.
- Keeps records as `draft` or `needs-decision` when required grounding items are missing.
- Produces executable records after the preflight instead of stopping at a checklist.
- Does not use the preflight as permission to start implementation without records, ledger rows, and a goal prompt.

Fail signs:

- Opens with a polished paragraph that sounds complete but lacks evidence, preview, acceptance, or verification.
- Marks records `ready` while several preflight items are missing.
- Treats the user's demand for "detailed blueprint" as a request for longer prose.

## Case 12: Target Mode Without Executable Control

Prompt:

```text
Use $blueprint-driven-project-runner. CRM has already been running for two days and still did not finish the target. Continue the target mode and finish it.
```

Pass criteria:

- Starts with `Target Mode Startup Gate: PASS / FAIL`.
- Fails closed if ready blueprint records, a bounded work slice, execution ledger rows, a scoped goal prompt, or an execution contract are missing.
- Does not edit product code when the gate fails.
- Routes to the smallest corrective mode: Blueprint Audit, Ledger Compiler, Goal Prompt, Status, or Recovery.
- For an old half-built project, compiles a minimal remaining-work blueprint from source evidence instead of trying to reconstruct all chat history.
- Requires the generated goal prompt to cite blueprint record IDs, work slice ID, ledger row IDs, allowed scope, forbidden scope, evidence, and stop condition.

Fail signs:

- Continues with a broad instruction such as "finish the CRM" or "continue optimizing".
- Runs implementation without a ledger row.
- Reports progress without accepted evidence.
- Keeps changing files while diagnosing why the previous target did not finish.
