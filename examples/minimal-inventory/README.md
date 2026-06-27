# Minimal Inventory Example

This example shows the shape of a ready executable blueprint record.

Use it to test the bundled tools:

```bash
python scripts/lint_blueprints.py --path examples/minimal-inventory/docs/ai-control/inventory/engineering-blueprint.md
python scripts/generate_goal_prompt.py --project examples/minimal-inventory --module "Inventory" --record INVENTORY-IMPORT-IDEMPOTENCY-001 --work-slice WS-IMPORT-001 --ledger-row LEDGER-INVENTORY-001
```

The example is intentionally generic and contains no private product, customer, or company data.
