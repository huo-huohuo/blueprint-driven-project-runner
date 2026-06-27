# Technical Blueprint Questionnaire

Use this reference when a blueprint touches backend, data, integration, automation, infrastructure, background jobs, or other technical areas. The goal is to let non-technical users confirm behavior without forcing them to design internals.

## Principle

The user provides business facts. The agent compiles technical contracts.

Do not ask the user to choose database tables, endpoints, queue names, or architecture patterns unless the choice changes product behavior, cost, risk, or ownership.

## User-Fill Questionnaire

Ask only the questions needed for the current slice. Prefer 5-8 focused questions over a full form.

```markdown
# Technical Blueprint Intake

## 1. Outcome

What should be different after this feature works?

## 2. Actor

Who or what starts the action?

- human user:
- system job:
- external system:
- AI agent:

## 3. Trigger

What event starts it?

## 4. Before State

What is true before the action starts? Give one concrete example.

## 5. Action

What happens during the action, in business language?

## 6. After State

What must be true after the action succeeds? Give one concrete example.

## 7. Forbidden Outcomes

What must never happen?

## 8. Repeated Action

If the same action happens twice, should the result be duplicated, ignored, updated, merged, or rejected?

## 9. Failure Behavior

If something goes wrong, what should the user or operator see? What should remain unchanged?

## 10. Boundaries

Which systems, files, screens, records, or data areas must this not touch?

## 11. Evidence

What would convince you this works?

- test:
- screenshot:
- before/after data:
- log:
- report:
- manual check:

## 12. Risk

Could this affect real users, money, production-like data, irreversible state, external systems, or large batches?
```

## AI Compilation Steps

After the questionnaire:

1. Restate the user's business scenario in plain language.
2. Separate confirmed facts from inferred technical details.
3. Read source code and docs to discover existing patterns.
4. Compile one or more executable blueprint records.
5. Put uncertain technical choices in `Open Questions` or `DECISION_NEEDED`.
6. Produce a technical preview checklist for user confirmation.

## Technical Preview Checklist

Use this before implementation. It is the backend equivalent of a frontend preview image.

```markdown
# Technical Preview: <record id>

## Business Flow

| Step | Actor/System | Action | Result |
| --- | --- | --- | --- |
| 1 | | | |

## Before / After Example

| Item | Before | After |
| --- | --- | --- |
| | | |

## Inputs And Outputs

| Operation | Input Example | Output / Effect |
| --- | --- | --- |
| | | |

## State Rules

| Current State | Action | Next State | Forbidden Next State |
| --- | --- | --- | --- |
| | | | |

## Boundaries

Will touch:
-

Must not touch:
-

## Failure Matrix

| Failure | Expected User/System Result | Must Remain True | Evidence |
| --- | --- | --- | --- |
| | | | |

## Evidence Plan

| Evidence | Method | Pass Condition |
| --- | --- | --- |
| | | |
```

## Executable Technical Record Shape

Use this shape inside the normal executable blueprint record:

```text
ID:
Type: engineering / data / integration / automation / infrastructure / safety / ops
Source:
Current Evidence:
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
Preview:
Acceptance:
Verification:
Owner:
Status:
Confidence:
Open Questions:
```

Use `Access Rule` only when actor visibility or allowed actions matter. Use `DECISION_NEEDED` rather than inventing sensitive rules.
