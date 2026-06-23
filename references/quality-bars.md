# Quality Bars and Failure Modes

Use this reference when deciding whether a large AI run is ready to execute, when auditing vague blueprints, or when recovering from drift.

## Common Failure Modes

| Failure | Symptom | Countermeasure |
| --- | --- | --- |
| summary blueprint | The "blueprint" is a polished paragraph with no ID, forbidden result, or verification. | Reclassify as discovery brief and compile executable records. |
| missing preview | Technical records describe internals but give the user no checklist, state table, or before/after example to confirm. | Add a user-checkable preview before execution. |
| aspiration prompt | The agent "improves" forever without a finish line. | Require executable records and acceptance evidence. |
| missing task ledger | The blueprint is ready, but execution starts from a broad prompt and progress is hard to judge. | Compile `docs/ai-control/91-execution-ledger.md` with row-level goals, paths, acceptance, verification, status, and skip/resume rules. |
| hidden product standard | The user can see the UI is wrong, but the prompt never encoded why. | Write interface records with states and forbidden UI. |
| unbounded edit radius | Many unrelated files change. | Use allowed and forbidden files in every execution contract. |
| context drift | Later runs contradict earlier decisions. | Put durable decisions in records or ADRs, not chat memory. |
| false progress | Big diffs look productive but no user workflow improves. | Report maturity movement only from evidence. |
| weak verification | The agent says "done" without testing the actual workflow. | Define evidence before implementation. |
| cross-thread collision | Two threads edit the same shared files. | Assign owners and serialize high-conflict areas. |
| evidence ambiguity | Simulated, draft, or inferred effects are mistaken for real effects. | Define evidence policy and pass/fail checks. |

## Blueprint Definition Of Ready

A record can authorize execution only when all are true:

- Required fields exist: `ID`, `Type`, `Source`, `Current Evidence`, `Target Behavior`, `Forbidden Result`, `Preview`, `Acceptance`, `Verification`, `Owner`, `Status`, `Confidence`, `Open Questions`.
- `ID` is stable and specific, not `BP-001` unless the project has no module names yet.
- `Source` cites user instruction, doc, code, screenshot, issue, or explicit inference.
- `Current Evidence` says what is true now, or `NOT_CHECKED`.
- `Target Behavior` has observable behavior, not adjectives.
- `Forbidden Result` blocks at least one known wrong direction.
- `Preview` is user-checkable: visual/state preview for UI, checklist/sample preview for technical work.
- `Acceptance` can pass or fail.
- `Verification` names a concrete method.
- `Status` is `ready` or `accepted`.
- `DECISION_NEEDED` appears only when the record is not ready.

## Vague Word Smells

These words are allowed only when paired with measurable criteria:

```text
optimize, improve, better, smart, intelligent, mature, clean, professional, complete, comprehensive, robust, seamless, easy, convenient, clear
优化, 完善, 更好, 智能, 成熟, 清晰, 高效, 方便, 美观, 专业, 完整, 全面, 稳定
```

Bad:

```text
The dashboard should be more professional and intelligent.
```

Good:

```text
Forbidden Result:
- The default dashboard must not show unrelated panels before the user selects a workflow.
Preview:
- State checklist showing initial, selected, empty, loading, and error states.
Acceptance:
- Screenshot of the default route shows one primary work queue, one filter bar, and no secondary panel.
Verification:
- Browser screenshot comparison.
```

## Technical Preview Quality Bar

Technical/backend records should include at least three of these preview elements:

- business flow checklist
- before/after data example
- input/output example
- state transition table
- boundary list
- failure matrix
- evidence plan

If a non-specialist cannot confirm the intended behavior from the preview, the record is not ready.

## Evidence Ladder

Prefer the strongest feasible evidence:

1. Static source inspection.
2. Syntax/type/lint check.
3. Unit or golden test.
4. Integration/API check.
5. Browser flow or screenshot comparison.
6. Representative real-data validation.
7. User acceptance.

When evidence is weak, narrow the claim. Say "syntax verified" instead of "feature complete".

## Good Execution Contract Test

A contract is good when another agent can answer these questions without reading chat history:

- What exact outcome should change?
- Which executable blueprint records authorize the change?
- Which execution ledger rows will be advanced?
- Which files are allowed?
- Which files are forbidden?
- What data writes are allowed?
- How will success be proven?
- When must the agent stop?

## Good Execution Ledger Test

A ledger is good when another agent can execute it row by row without asking for a new plan:

- Each row has a stable ID.
- Each row cites blueprint record IDs and a work slice.
- The goal is a concrete outcome, not a theme.
- The completion path says what to do in order.
- Scope or files are explicit enough to prevent wandering.
- Acceptance can pass or fail.
- Verification names a command, check, screenshot, API check, sample, or manual evidence.
- Status is one of `planned`, `active`, `blocked`, `shelved`, `skipped`, `verified`, or `accepted`.
- Blocked/shelved/skipped rows include a reason and resume condition.

## Signs A Slice Is Too Large

- It mixes product decisions with architecture decisions.
- It requires more than one owner to edit shared files.
- It cannot be verified without several unrelated checks.
- The unknowns are still larger than the implementation.
- It has no obvious user-visible or system-visible stopping point.

## Recovery Classification

When reviewing a messy run, classify each changed file:

- **contracted**: directly required by the execution contract
- **supporting**: not named but clearly necessary and low risk
- **useful-uncontracted**: possibly valuable, but should be moved to backlog or separately reviewed
- **suspicious**: likely drift, regression, or accidental edit
- **unrelated**: must not be touched further without user instruction

Do not revert suspicious or unrelated changes blindly. First identify whether they came from the user, another thread, or this run.

## Public-Quality Skill Bar

A publishable project-control skill should be:

- narrow enough to trigger for large AI project control, not every coding task
- explicit about when not to code
- strict about summary versus executable blueprint records
- source-aware instead of chat-memory-dependent
- enforceable through templates and linting
- light enough that agents will actually follow it
