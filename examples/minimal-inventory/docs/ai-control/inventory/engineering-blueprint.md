# Engineering Blueprint: Inventory

## Executable Blueprint Records

### INVENTORY-IMPORT-IDEMPOTENCY-001 import idempotency

ID: INVENTORY-IMPORT-IDEMPOTENCY-001
Type: engineering
Source:
- Example requirement: repeated imports should not duplicate records.
Current Evidence:
- The import flow accepts records with an external key.
Target Behavior:
- Business Scenario: a user imports records from a file or external system.
- Actor: human user or scheduled job.
- Trigger: import starts with a staged batch.
- Before State: item may or may not already exist by external key.
- Action: import validates and creates, updates, or skips each item.
- After State: repeated import leaves one final record for each external key.
- System Boundary: import modifies only the declared target collection.
- Data Contract: each item has external_key and payload fields.
- Operation Contract: same input twice reaches the same final state.
- Access Rule: actor must be allowed to run this import operation.
- Repeat/Idempotency Rule: duplicate input is skipped or merged, not duplicated.
- Failure Behavior: invalid items are reported without corrupting valid items.
- Observability: result includes created, updated, skipped, and failed counts.
Forbidden Result:
- Do not create duplicate records for the same external key.
- Do not alter unrelated collections.
Preview:
- business flow: receive -> validate -> create/update/skip -> report counts.
- before/after: missing key creates a record; existing key updates or skips; invalid row is rejected.
- state table: staged -> processed / rejected.
- boundary list: target collection only; no unrelated collections.
- failure matrix: invalid row, duplicate row, interrupted run.
- evidence plan: golden test plus local fixture result.
Acceptance:
- Importing the same valid item twice leaves one final business record.
- Invalid item is reported and does not alter unrelated records.
Verification:
- Unit/golden test against local fixture data.
Owner: backend owner
Status: ready
Confidence: high
Open Questions:
- None.
