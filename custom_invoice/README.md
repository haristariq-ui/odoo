# Customer Balance on Invoice

## Overview
This custom Odoo module extends the **Customer Invoice (`account.move`)** model by adding two computed monetary fields:

- **Previous Balance** – Displays the total outstanding balance of all previously posted customer invoices for the same customer.
- **Current Balance** – Displays the customer's total balance after including the current invoice's outstanding amount.

These fields help accountants and sales teams quickly view a customer's financial position directly from the invoice.

---

## Features

- Adds **Previous Balance** field.
- Adds **Current Balance** field.
- Automatically recalculates balances whenever:
  - Customer changes
  - Invoice total changes
  - Residual amount changes
- Supports multiple currencies using the invoice currency.
- Stored computed fields for better reporting and searching.

---

## Model Extension

The module inherits the following model:

```python
account.move
```

---

## Added Fields

### Previous Balance

| Property | Value |
|----------|-------|
| Field Name | `previous_balance` |
| Type | Monetary |
| Stored | Yes |
| Computed | `_compute_previous_balance` |

**Description**

Calculates the total outstanding amount (`amount_residual`) of all posted customer invoices belonging to the same customer, excluding the current invoice.

Only invoices that satisfy the following conditions are considered:

- Customer is the same
- Invoice type is Customer Invoice (`out_invoice`)
- Invoice is Posted
- Remaining amount is greater than zero
- Current invoice is excluded

---

### Current Balance

| Property | Value |
|----------|-------|
| Field Name | `current_balance` |
| Type | Monetary |
| Stored | Yes |
| Computed | `_compute_current_balance` |

**Description**

Calculates the customer's balance including the current invoice.

Formula:

```
Current Balance = Previous Balance + Current Invoice Residual
```

If the invoice has not yet been posted, only the previous balance is displayed.

---

## Compute Methods

### `_compute_previous_balance()`

Dependencies:

```python
partner_id
amount_total
amount_residual
```

Workflow:

1. Initialize previous balance to `0.0`.
2. Search for all posted customer invoices of the same customer.
3. Exclude the current invoice.
4. Ignore invoices with zero residual.
5. Sum the remaining residual amounts.
6. Store the result in `previous_balance`.

---

### `_compute_current_balance()`

Dependencies:

```python
previous_balance
amount_residual
```

Workflow:

- If invoice is **Posted**

```
Current Balance = Previous Balance + Current Invoice Residual
```

- Otherwise

```
Current Balance = Previous Balance
```

---

## Example

Suppose Customer **ABC Traders** has the following invoices:

| Invoice | Status | Residual |
|----------|--------|---------:|
| INV001 | Posted | 15,000 |
| INV002 | Posted | 8,000 |
| INV003 (Current) | Posted | 12,000 |

The computed values will be:

```
Previous Balance = 23,000
Current Balance  = 35,000
```

---

## Dependencies

- `account`

---

## Benefits

- Provides quick visibility of customer outstanding balances.
- Eliminates the need to manually calculate unpaid invoices.
- Improves decision-making before validating new invoices.
- Useful for finance, accounting, and credit management.

---

## Notes

- Only **posted customer invoices** are considered.
- Vendor bills and other journal entries are ignored.
- Fully paid invoices (Residual = 0) are excluded.
- The current invoice is excluded from the previous balance calculation to avoid duplication.

---

## Author

Developed as a customization for **Odoo Accounting (`account.move`)** to display customer outstanding balances directly on invoices.