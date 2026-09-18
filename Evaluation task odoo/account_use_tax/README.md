# Account Use Tax

An Odoo 19 accounting module that introduces a custom **Use Tax** type and displays Use Tax information in the standard **Tax Report**.

The module extends Odoo's existing tax system and reporting framework without creating a separate tax model or separate reporting interface.

---

## Features

- Adds a new **Use** option to the Tax Type field
- Allows users to create taxes specifically for Use Tax
- Integrates Use Taxes into the standard Odoo Tax Report
- Displays Use Tax as a separate **Use** section
- Groups Use Tax data by individual tax
- Calculates:
  - Net amount
  - Tax amount
- Supports multiple Use Taxes
- Respects the report's selected date range
- Supports reports involving multiple companies
- Includes an audit action for Use Tax report cells
- Works with active and archived Use Taxes

---

## Module Structure

```text id="y4q8hp"
account_use_tax/
│
├── __init__.py
├── __manifest__.py
│
└── models/
    ├── __init__.py
    ├── account_tax.py
    └── generic_tax_report_handler.py
```

---

## Dependencies

The module depends on:

```python id="3k2qgz"
'account',
'account_reports',
```

### `account`

Provides:

- Taxes
- Journal entries
- Journal items
- Accounting moves

### `account_reports`

Provides Odoo's accounting report framework, including the generic tax report handler.

---

# 1. Adding the Use Tax Type

The standard Odoo `account.tax` model is extended:

```python id="qj8f8m"
class AccountTax(models.Model):
    _inherit = 'account.tax'
```

The existing `type_tax_use` selection field is extended with:

```python id="9q0y7e"
type_tax_use = fields.Selection(
    selection_add=[
        ('use', 'Use'),
    ],
    ondelete={
        'use': 'set default',
    },
)
```

This adds:

```text
Use
```

as an additional tax type.

---

## Tax Type

The standard tax usage options can contain options such as:

```text
Sales
Purchases
None
```

This module adds:

```text
Use
```

A tax configured with:

```text
Tax Type = Use
```

is treated as a Use Tax by the custom report logic.

---

## `ondelete`

The selection extension includes:

```python id="f4jzv4"
ondelete={
    'use': 'set default',
}
```

This provides fallback behavior if the custom selection value is removed while records are still using it.

---

# 2. Custom Tax Report Handler

The module extends:

```python id="z9ckhy"
account.generic.tax.report.handler
```

using:

```python id="6w0y7e"
class GenericTaxReportCustomHandler(models.AbstractModel):
    _inherit = 'account.generic.tax.report.handler'
```

The main customization is implemented in:

```python id="x2dj7r"
_dynamic_lines_generator()
```

The method extends Odoo's existing dynamic tax report lines rather than replacing the standard report completely.

---

## Preserving Standard Tax Report Data

The first step is:

```python id="k8k0n9"
dynamic_lines = list(
    super()._dynamic_lines_generator(
        report,
        options,
        all_column_groups_expression_totals,
        warnings=warnings
    )
)
```

This calls Odoo's original implementation first.

Therefore:

```text
Standard Tax Report
       │
       ▼
Odoo generates normal tax lines
       │
       ▼
Custom module adds Use Tax section
```

The existing Odoo tax report remains available, while the new Use Tax information is appended.

---

# 3. Finding Use Taxes

The module searches for taxes where:

```python id="h5a3b7"
type_tax_use = 'use'
```

The search is performed using:

```python id="4i1y2s"
use_taxes = self.env['account.tax'].with_context(
    active_test=False
).search([
    ('type_tax_use', '=', 'use')
])
```

### Why `active_test=False`?

Normally, Odoo searches only active records.

Using:

```python
with_context(active_test=False)
```

allows the report logic to also find archived Use Taxes.

---

# 4. Company Filtering

The report determines which companies are included:

```python id="o9o4cs"
company_ids = (
    report.get_report_company_ids(options)
    if hasattr(report, 'get_report_company_ids')
    else self.env.companies.ids
)
```

If the report provides `get_report_company_ids()`, those companies are used.

Otherwise, the current environment companies are used.

This makes the customization compatible with report configurations where multiple companies are selected.

---

# 5. Finding Relevant Journal Items

The module searches:

```python id="0qf1l5"
account.move.line
```

Only posted accounting entries are considered:

```python id="9x3m6h"
('parent_state', '=', 'posted')
```

The company must also be included:

```python id="o7jv3n"
('company_id', 'in', company_ids)
```

The important condition is:

```python id="w2c6t1"
'|',
('tax_ids', 'in', use_taxes.ids),
('tax_line_id', 'in', use_taxes.ids),
```

This means a journal item is relevant if a Use Tax is found either:

- In `tax_ids`, or
- In `tax_line_id`

---

# 6. Date Range

The report reads the selected dates from the report options:

```python id="3p7n4c"
date_from = options.get('date', {}).get('date_from')
date_to = options.get('date', {}).get('date_to')
```

If a start date exists:

```python id="b7j2t5"
domain.append(('date', '>=', date_from))
```

If an end date exists:

```python id="g1w8q9"
domain.append(('date', '<=', date_to))
```

Therefore, the Use Tax section follows the date range selected in the Tax Report.

---

# 7. Calculating Use Tax Data

The module creates a dictionary for each Use Tax:

```python id="k9q3z6"
tax_data = defaultdict(
    lambda: {
        'net': 0.0,
        'tax': 0.0
    }
)
```

Each Use Tax stores two values:

```text
net → Net amount
tax → Tax amount
```

---

## Tax Amount

If the journal item itself represents a Use Tax line:

```python id="w4e6n8"
if aml.tax_line_id and aml.tax_line_id.type_tax_use == 'use':
    tax_data[aml.tax_line_id]['tax'] += aml.balance
```

Its balance is added to the tax amount.

Example:

```text
Use Tax: 15%

Tax Line Balance = 150

Tax Amount = 150
```

---

## Net Amount

The module also checks the taxes applied to each journal item:

```python id="r8d2k5"
for applied_tax in aml.tax_ids:
    if applied_tax.type_tax_use == 'use':
        tax_data[applied_tax]['net'] += aml.balance
```

The journal item's balance is added to the corresponding Use Tax's net amount.

---

# 8. Use Tax Report Section

A separate report section is created:

```text
Use
```

The section receives a unique report line ID:

```python id="t5m7x2"
section_id = report._get_generic_line_id(
    None,
    None,
    markup='use_section'
)
```

The section is displayed at:

```text
Level 1
```

while individual taxes are displayed underneath it at:

```text
Level 2
```

---

## Example Report Structure

```text
Tax Report
│
├── Sales Taxes
│   ├── VAT 15%
│   └── VAT 5%
│
├── Purchase Taxes
│   ├── Input VAT
│   └── Purchase Tax
│
└── Use
    ├── Use Tax 5%
    ├── Use Tax 10%
    └── Use Tax 15%
```

---

# 9. Individual Use Tax Lines

For every Use Tax found in `tax_data`, the module creates a report line.

The label is generated as:

```python id="c6x4p9"
tax_label = (
    f"{tax.name} ({tax.amount}%)"
    if tax.amount
    else tax.name
)
```

For example:

```text
Use Tax (15%)
```

If the tax has no percentage amount, only its name is displayed.

---

# 10. Net and Tax Columns

The module checks the report column's:

```python id="f7u2k1"
expression_label
```

The value is selected accordingly:

```python id="p8v3m6"
val = (
    tax_val
    if expr_label == 'tax'
    else (
        net_val
        if expr_label == 'net'
        else 0.0
    )
)
```

Therefore:

```text
expression_label = net
        ↓
Net Amount

expression_label = tax
        ↓
Tax Amount
```

Other expression labels receive:

```text
0.0
```

---

# 11. Use Tax Total

The module maintains a total tax amount:

```python id="h2j6q4"
total_tax_amount = 0.0
```

For every Use Tax:

```python id="m6n8r3"
total_tax_amount += tax_val
```

The total is then displayed on the **Use** section.

Example:

```text
Use
--------------------------------
Use Tax 5%       Net: 1,000  Tax: 50
Use Tax 10%      Net: 2,000  Tax: 200
Use Tax 15%      Net: 1,000  Tax: 150
--------------------------------
Total Tax                         400
```

---

# 12. Audit Action

Each individual Use Tax line includes:

```python id="j8p3v5"
'action': 'action_audit_cell'
```

and:

```python id="n4c7x1"
'action_params': {
    'report_line_id': line_id,
    'expression_label': 'tax',
    'column_group_key': (
        options['columns'][0]['column_group_key']
        if options.get('columns')
        else None
    ),
}
```

This allows the report line to use Odoo's audit functionality for the tax amount.

Users can therefore investigate the accounting entries behind the reported amount.

---

# 13. Report Behavior

If no Use Taxes exist:

```python
if not use_taxes:
    return dynamic_lines
```

The standard report is returned unchanged.

Similarly, if there are no matching journal items:

```python
if not move_lines:
    return dynamic_lines
```

No empty Use Tax section is added.

This means the custom section appears only when relevant Use Tax data exists.

---

# Complete Flow

```text
Create Use Tax
      │
      ▼
Tax Type = Use
      │
      ▼
Post Accounting Transactions
      │
      ▼
Open Odoo Tax Report
      │
      ▼
Odoo Generates Standard Tax Lines
      │
      ▼
Custom Handler Searches for Use Taxes
      │
      ▼
Find Posted Journal Items
      │
      ▼
Apply Company + Date Filters
      │
      ▼
Calculate Net & Tax Amounts
      │
      ▼
Create "Use" Section
      │
      ▼
Create Individual Use Tax Lines
      │
      ▼
Display Tax Report
```

---

## Example

Suppose a company has a Use Tax:

```text
Name: Use Tax
Type: Use
Rate: 15%
```

And the accounting data produces:

```text
Net Amount: 10,000
Tax Amount: 1,500
```

The Tax Report can display:

```text
Use
│
└── Use Tax (15%)     Net: 10,000    Tax: 1,500

Total Tax: 1,500
```

---

## Installation

1. Copy the module into your Odoo custom addons directory.

2. Restart the Odoo server.

3. Update the Apps List.

4. Search for:

```text
Account Use Tax
```

5. Install the module.

---

## Usage

### Step 1 — Create a Use Tax

Go to:

```text
Accounting → Configuration → Taxes
```

Create or edit a tax.

Set:

```text
Tax Type → Use
```

Configure the required tax rate and other tax settings.

---

### Step 2 — Use the Tax

Apply the Use Tax to the appropriate accounting transaction.

Post the resulting accounting entry.

---

### Step 3 — Open the Tax Report

Go to the Accounting reporting section and open the relevant Tax Report.

Select the required date range.

The report will include a:

```text
Use
```

section when matching Use Tax accounting data exists.

---

## Technical Details

| Item | Value |
|---|---|
| Odoo Version | 19.0 |
| Module Name | Account Use Tax |
| Main Tax Model | `account.tax` |
| Report Handler | `account.generic.tax.report.handler` |
| Journal Item Model | `account.move.line` |
| Dependencies | `account`, `account_reports` |
| License | LGPL-3 |
| Author | Muhammad Haris |

---

## Manifest

```python id="c8v4m2"
{
    'name': 'Account Use Tax',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'author': 'Muhammad Haris',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'account_reports',
    ],
    'installable': True,
    'application': False,
}
```

---

## License

This module is licensed under the **LGPL-3** license.