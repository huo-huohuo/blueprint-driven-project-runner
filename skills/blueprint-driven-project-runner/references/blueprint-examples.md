# Executable Blueprint Examples

Use these examples when the agent is producing summary-like blueprints. The point is not the domain; the point is the structure, preview, and testability.

## Example 1: Frontend Initial State

```text
ID: WORK-QUEUE-INITIAL-001
Type: interface
Source: User instruction: default route should open on a focused work queue, not a mixed detail view.
Current Evidence:
- NOT_CHECKED
Target Behavior:
- Opening the default route shows one primary list or queue as the main content.
- Detail, editor, and assistant panels remain hidden until the user selects an item.
- Each row shows the minimum fields needed to decide the next action.
Forbidden Result:
- Do not show a detail panel before selection.
- Do not duplicate the same navigation actions in multiple regions.
Preview:
- State checklist: initial list, selected item, empty list, loading state, error state.
- Static preview or screenshot reference required before implementation.
Acceptance:
- Screenshot of the default route before selection shows the main queue and no detail/editor panel.
Verification:
- Browser screenshot or Playwright screenshot.
Owner: frontend owner
Status: draft
Confidence: medium
Open Questions:
- DECISION_NEEDED: exact row density and minimum visible fields.
```

## Example 2: Data Import Idempotency

```text
ID: DATA-IMPORT-IDEMPOTENCY-001
Type: engineering
Source: User instruction: repeated imports should not create duplicate business records.
Current Evidence:
- Existing import behavior has not been checked.
Target Behavior:
- Business Scenario: a user or job imports records from an external file or system.
- Actor: human user or scheduled job.
- Trigger: import starts with a file, API response, or staged batch.
- Before State: record with unique external key may or may not already exist.
- Action: import validates, maps, and writes records.
- After State: new records are created; existing records are updated or skipped according to the chosen rule.
- System Boundary: import must not modify unrelated modules.
- Data Contract: each imported item has a stable identity key.
- Operation Contract: repeated import with the same identity key does not create duplicate rows.
- Access Rule: DECISION_NEEDED if actor restrictions matter.
- Repeat/Idempotency Rule: same input twice produces the same final state.
- Failure Behavior: invalid rows are reported without corrupting valid existing records.
- Observability: import result records created, updated, skipped, failed counts.
Forbidden Result:
- Do not create duplicate records for the same identity key.
- Do not partially corrupt existing records when one row fails validation.
Preview:
- Business flow checklist: receive input -> validate -> map -> create/update/skip -> report.
- Before/after table for one new item, one existing item, and one invalid item.
- Failure matrix for invalid input, duplicate input, and interrupted import.
Acceptance:
- Golden case: importing the same valid item twice leaves one final business record.
- Golden case: invalid item is reported and does not alter unrelated records.
Verification:
- Unit/golden test or local integration test.
Owner: backend owner
Status: ready
Confidence: high
Open Questions:
- None.
```

## Example 3: Background Job Failure Behavior

```text
ID: JOB-RETRY-FAILURE-001
Type: ops
Source: User instruction: automated work should be reliable and inspectable.
Current Evidence:
- NOT_CHECKED
Target Behavior:
- Business Scenario: a background job processes a batch of pending items.
- Actor: scheduled job.
- Trigger: timer, queue event, or manual run.
- Before State: pending items exist.
- Action: job processes each item and records outcome.
- After State: successful items are marked complete; failed items remain retryable or move to a clear failure state.
- System Boundary: job must not process items outside its declared scope.
- Repeat/Idempotency Rule: rerunning the job does not duplicate completed effects.
- Failure Behavior: failure is logged and visible without hiding unprocessed items.
- Observability: run id, start/end time, counts, failures, and next retry state are recorded.
Forbidden Result:
- Do not silently drop failed items.
- Do not mark an item complete before the external or internal effect is confirmed.
Preview:
- State table: pending -> processing -> complete / retryable / failed.
- Failure matrix: timeout, invalid item, dependency unavailable, repeated run.
- Evidence plan: run log plus sample item state before and after.
Acceptance:
- Golden case: failed item remains visible with failure reason and can be retried or inspected.
- Golden case: rerun after success does not duplicate completed effects.
Verification:
- Job test, local run against fixture data, or log inspection.
Owner: operations owner
Status: needs-decision
Confidence: medium
Open Questions:
- DECISION_NEEDED: retry limit and final failure state.
```
