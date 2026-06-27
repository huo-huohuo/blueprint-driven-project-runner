# From Vague Goal To Executable Blueprint

This example shows the packaging difference between a normal long-running AI prompt and a blueprint-driven run.

## Vague Request

```text
Use Codex to optimize the CRM interface.
Make it more professional, complete, convenient, and suitable for long-term use.
```

This is not executable yet. It has no source evidence, no states, no forbidden result, no acceptance, and no verification.

## Blueprint Grounding Preflight

Source evidence: User instruction says the CRM interface should be improved before long-running execution.

Current state checked or NOT_CHECKED: NOT_CHECKED.

Observable target behavior: The default CRM route shows a focused customer work queue before any customer is selected.

Forbidden outcomes:

- Do not show a detail, editor, or assistant panel before the user selects a customer.
- Do not duplicate the same navigation action in multiple regions.
- Do not claim the interface is complete without screenshot or browser-flow evidence.

User-checkable preview:

- Initial state: one primary customer queue is visible.
- Loading state: the queue area shows loading feedback without layout shift.
- Empty state: the queue area explains there are no customers in the selected filter.
- Selected state: selecting one customer opens the detail region.
- Error state: the queue area shows a recoverable error state.

Pass/fail acceptance: A screenshot of the default route before selection passes only if it shows one primary work queue and no detail/editor panel.

Verification method: Browser screenshot or Playwright screenshot.

DECISION_NEEDED items:

- Exact CRM route path.
- Minimum row fields required for the queue.
- Visual density target.

Execution allowed: no. Records with open decisions stay `draft` or `needs-decision`.

## Executable Blueprint Record

ID: CRM-QUEUE-INITIAL-001
Type: interface
Source:

- User instruction: optimize CRM interface before broad execution.

Current Evidence:

- NOT_CHECKED.

Target Behavior:

- Opening the default CRM route shows one primary customer work queue as the main content.
- Detail, editor, and assistant panels remain hidden until a customer row is selected.
- The queue exposes enough fields for a user to choose the next customer action.
- Initial, loading, empty, selected, and error states are defined before implementation.

Forbidden Result:

- Do not show customer detail before selection.
- Do not replace the work queue with a dashboard-style collection of unrelated cards.
- Do not mark the interface ready without screenshot or browser-flow evidence.

Preview:

- State checklist: initial queue, loading queue, empty queue, selected customer detail, recoverable error.
- Layout contract: default route has one primary queue region; secondary regions are hidden until selection.
- Evidence preview: screenshot path or browser-check output is recorded in the ledger row.

Acceptance:

- Default route screenshot before selection shows one primary queue and no detail/editor panel.
- Selecting a customer opens exactly one detail region.
- Empty, loading, and error states do not overlap the queue controls.

Verification:

- Browser screenshot or Playwright screenshot.

Owner: frontend owner
Status: needs-decision
Confidence: medium
Open Questions:

- DECISION_NEEDED: CRM route path.
- DECISION_NEEDED: required row fields.

## Execution Ledger Row

| ID | Blueprint Records | Work Slice | Goal | Completion Path | Scope / Files | Acceptance Standard | Verification Method | Evidence | Status | Accepted? | Blocker / Skip Reason | Resume Condition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LEDGER-CRM-001 | CRM-QUEUE-INITIAL-001 | WS-CRM-QUEUE-INITIAL | Implement default CRM queue state | Confirm route and row fields, update layout, run browser check, attach screenshot | CRM route and queue components only | Default route shows one primary queue and no detail panel before selection | Browser screenshot | TBD | blocked | no | Route and row-field decisions missing | Resume after route path and minimum row fields are confirmed |

## Goal Prompt Shape

```text
First principle:
Complete CRM-QUEUE-INITIAL-001 and LEDGER-CRM-001 exactly, with evidence.
Do not optimize adjacent CRM areas, redesign unrelated navigation, or rewrite shared modules.

Read first:
- AGENTS.md
- docs/ai-control/00-operating-standard.md
- docs/ai-control/91-execution-ledger.md

Stop condition:
Stop when LEDGER-CRM-001 is accepted, blocked with a resume condition, or found to exceed the allowed scope.
```

## Why This Matters

The vague request encourages broad editing. The executable blueprint defines the judging system before implementation, so the agent knows what to build, what not to build, how to prove it, and when to stop.
