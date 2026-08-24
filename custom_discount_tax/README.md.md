# Discount and Tax Amount on Customer Invoices

## Overview

This Odoo customization adds **Discount Amount** and **Tax Amount** fields to customer invoice lines.

It also ensures that the values calculated on **Sale Order Lines** are automatically transferred to the corresponding **Customer Invoice Lines** when the **Create Invoice** button is clicked from a sale order.

## Features

- Adds **Discount Amount** to customer invoice lines.
- Adds **Tax Amount** to customer invoice lines.
- Automatically calculates the discount amount based on:
  - Quantity
  - Unit Price
  - Discount percentage
- Automatically calculates the tax amount based on:
  - Taxable amount after discount
  - First tax configured on the line
- Transfers the discount and tax amounts from sale order lines to invoice lines.
- Displays the new fields in the customer invoice line view.

## Module Structure

```text
discount_tax_amount/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── account_move_line.py
│   └── sale_order_line.py
└── views/
    └── account_move_line.xml
```

## Dependencies

The module depends on:

- `account`
- `sale`
- `sale_purchase_custom`

## Implementation

### 1. Invoice Line Fields

The module inherits `account.move.line` and adds two computed monetary fields:

- `discount_amount`
- `tax_amount`

The values are calculated using `_compute_discount_tax_amount()`.

### Discount Calculation

The gross amount is calculated as:

```text
gross amount = quantity × unit price
```

The discount amount is:

```text
discount amount = gross amount × discount percentage ÷ 100
```

### Tax Calculation

After calculating the discount:

```text
taxable amount = gross amount - discount amount
```

The tax amount is then calculated using the first tax assigned to the invoice line:

```text
tax amount = taxable amount × tax percentage ÷ 100
```

The computed fields are stored in the database using `store=True`.

## 2. Sale Order to Invoice Data Transfer

The module inherits `sale.order.line` and overrides:

```python
_prepare_invoice_line()
```

The original Odoo method is first called using `super()` so that the standard invoice-line values are preserved.

The customization then adds:

```python
{
    "discount_amount": self.discount_amount,
    "tax_amount": self.tax_amount,
}
```

Therefore, when a sale order is invoiced, the calculated values from the sale order line are included in the newly created invoice line.

## 3. Invoice View Changes

The customer invoice form view is inherited from:

```text
account.view_move_form
```

The XML customization:

- Makes the existing **Discount** column visible.
- Adds **Discount Amount** after the Discount field.
- Adds **Tax Amount** after the Taxes field.
- Makes Tax Amount readonly.

## Flow

```text
Sale Order
    │
    ▼
Sale Order Line
    │
    │ Calculate discount_amount
    │ Calculate tax_amount
    │
    ▼
Click "Create Invoice"
    │
    ▼
_prepare_invoice_line()
    │
    │ Copy discount_amount
    │ Copy tax_amount
    │
    ▼
Customer Invoice
    │
    ▼
Invoice Lines
    ├── Discount
    ├── Discount Amount
    ├── Taxes
    └── Tax Amount
```

## Example

Suppose a sale order line contains:

```text
Quantity       = 10
Unit Price     = 100
Discount       = 10%
Tax            = 15%
```

### Gross Amount

```text
10 × 100 = 1,000
```

### Discount Amount

```text
1,000 × 10 / 100 = 100
```

### Taxable Amount

```text
1,000 - 100 = 900
```

### Tax Amount

```text
900 × 15 / 100 = 135
```

The invoice line will therefore contain:

```text
Discount Amount = 100
Tax Amount      = 135
```

## Installation

1. Place the module inside the Odoo custom addons directory.
2. Restart the Odoo server.
3. Enable Developer Mode.
4. Go to **Apps**.
5. Update the Apps List.
6. Search for **Discount and Tax**.
7. Install the module.

## Testing

To test the module:

1. Create a quotation.
2. Add a product to the sale order.
3. Set a quantity and unit price.
4. Apply a discount.
5. Apply a tax.
6. Confirm the sale order.
7. Click **Create Invoice**.
8. Open the generated customer invoice.
9. Check the invoice lines.
10. Verify that **Discount Amount** and **Tax Amount** are automatically populated.

