# Journal Balance Custom

## Overview

Custom Odoo 19 module that extends the **Account Journal Dashboard**.

It adds a custom **Balance** field and displays:

**Balance = Current Statement Balance + Outstanding Payments**

It also renames the existing dashboard **Balance** label to **Unreconcile Balance**.

## Features

- Adds `balance` field to `account.journal`.
- Calculates balance for Bank, Cash, and Credit journals.
- Includes outstanding payments in the balance.
- Displays the custom Balance on the journal Kanban dashboard.
- Uses XPath inheritance to customize the standard Odoo journal dashboard.

## Files

```text
journal_balance_custom/
├── models/
│   ├── __init__.py
│   └── account_journal.py
├── views/
│   └── account_journal_views.xml
├── __init__.py
└── __manifest__.py
```

## Dependencies

```text
account
```

## Calculation

```text
Current Statement Balance
          +
Outstanding Payments
          =
Custom Balance
```

## Version

**Odoo:** 19.0  
**Category:** Accounting  
**Author:** Muhammad Haris