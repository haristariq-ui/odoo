# Contact History

## Overview

**Contact History** is a custom Odoo module that maintains a history of a customer's confirmed sales orders and related invoices.

The module adds a **Contact History** menu under the Contacts configuration menu. A user can select a partner and view:

- Confirmed Sales Orders
- Products purchased by the partner
- Product descriptions
- Unit prices
- Quantities
- Customer invoices
- Customer refunds

The history can also be synchronized manually using the **Sync Contact History** server action.

Additionally, whenever a Sales Order is confirmed, its order lines are automatically added to the corresponding Contact History.

---

## Features

### 1. Contact History

A `contact.history` record is created for a customer/partner.

Each history record contains:

- Partner Name
- History Lines
- Invoices

---

### 2. Sales Order History

The module collects sales order information for the selected partner.

Only Sales Orders with:

```python
state = 'sale'
```

are included during synchronization.

For every order line, the following information is stored:

| Field | Description |
|---|---|
| Source Document | Sales Order from which the line came |
| Product Name | Product purchased |
| Description | Sales Order Line description |
| Unit Price | Price of one unit |
| Product Quantity | Quantity ordered |

---

### 3. Invoice History

The module also retrieves customer invoices and refunds belonging to the selected partner.

The following invoice types are included:

```python
'out_invoice'
'out_refund'
```

The invoice list displays:

| Field | Description |
|---|---|
| Invoice | Invoice number |
| Invoice Date | Date of the invoice |
| Total | Total invoice amount |
| Status | Current invoice status |

---

## Module Structure

A typical module structure is:

```text
contact_history/
│
├── __init__.py
├── __manifest__.py
│
├── models/
│   ├── __init__.py
│   ├── contact_history.py
│   └── sale_order.py
│
├── security/
│   └── ir.model.access.csv
│
└── views/
    └── contact_history_views.xml
```

---

# Models

## 1. Contact History Model

Model:

```python
contact.history
```

The model stores the history of a partner.

### Fields

#### `partner_id`

```python
partner_id = fields.Many2one(
    'res.partner',
    string='Partner Name',
    required=True,
)
```

Links the history record to an Odoo Contact/Partner.

Because it is `required=True`, every Contact History record must have a partner.

---

#### `history_line_ids`

```python
history_line_ids = fields.One2many(
    'contact.history.line',
    'history_id',
    string='History Lines'
)
```

Contains the sales history lines belonging to the Contact History.

The relationship is:

```text
contact.history
       |
       | One2many
       ↓
contact.history.line
```

---

#### `invoice_ids`

```python
invoice_ids = fields.Many2many(
    'account.move',
    'contact_history_invoice_rel',
    'history_id',
    'invoice_id',
    string='Invoices',
    domain=[
        ('move_type', 'in', ['out_invoice', 'out_refund'])
    ],
)
```

Stores invoices and refunds related to the partner.

The Many2many relationship uses the intermediate table:

```text
contact_history_invoice_rel
```

The domain limits the selectable records to:

```text
Customer Invoice → out_invoice
Customer Refund  → out_refund
```

---

# Contact History Line Model

Model:

```python
contact.history.line
```

This model stores individual product lines from confirmed Sales Orders.

### Fields

| Field | Type | Purpose |
|---|---|---|
| `history_id` | Many2one | Parent Contact History |
| `sale_order_id` | Many2one | Source Sales Order |
| `product_id` | Many2one | Product |
| `description` | Char | Order line description |
| `unit_price` | Float | Product unit price |
| `product_quantity` | Float | Ordered quantity |

The relationship is:

```text
Contact History
      │
      │ One2many
      ↓
Contact History Line
      │
      ├── Sales Order
      ├── Product
      ├── Description
      ├── Unit Price
      └── Quantity
```

---

# Synchronization

The main synchronization method is:

```python
action_sync_history()
```

It performs two main operations:

1. Synchronizes confirmed Sales Orders.
2. Synchronizes customer invoices/refunds.

---

## Step 1: Get the Partner

The method first gets the partner from the Contact History:

```python
partner = history.partner_id
```

If no partner exists, the record is skipped:

```python
if not partner:
    continue
```

---

## Step 2: Remove Existing History Lines

Before rebuilding the history, existing lines are deleted:

```python
history.history_line_ids.unlink()
```

This prevents old sales history lines from remaining after synchronization.

The history is therefore rebuilt from the current confirmed Sales Orders.

---

## Step 3: Search Confirmed Sales Orders

The module searches for Sales Orders belonging to the selected partner:

```python
sale_orders = SaleOrder.search(
    [
        ('partner_id', '=', partner.id),
        ('state', '=', 'sale'),
    ],
    order='date_order desc, id desc',
)
```

This means:

```text
Partner = selected partner
AND
State = Sales Order
```

The newest orders are processed first.

---

## Step 4: Process Order Lines

For every Sales Order:

```python
for order in sale_orders:
    for line in order.order_line:
```

the module goes through every Sales Order Line.

Lines without a product are ignored:

```python
if not line.product_id:
    continue
```

A new `contact.history.line` is then created containing:

```python
{
    'history_id': history.id,
    'sale_order_id': order.id,
    'product_id': line.product_id.id,
    'description': line.name,
    'unit_price': line.price_unit,
    'product_quantity': line.product_uom_qty,
}
```

---

# Invoice Synchronization

The module searches for customer invoices and refunds:

```python
invoices = AccountMove.search(
    [
        ('partner_id', '=', partner.id),
        ('move_type', 'in', [
            'out_invoice',
            'out_refund',
        ]),
    ],
    order='invoice_date desc, id desc',
)
```

The resulting invoices are assigned to:

```python
history.invoice_ids
```

using:

```python
history.invoice_ids = [(6, 0, invoices.ids)]
```

### Meaning of `(6, 0, ids)`

Odoo's Many2many command:

```python
(6, 0, ids)
```

means:

> Replace the existing Many2many records with the records whose IDs are provided.

For example:

```python
history.invoice_ids = [(6, 0, [10, 15, 20])]
```

means the history will contain invoices:

```text
Invoice 10
Invoice 15
Invoice 20
```

---

# Automatic History Creation on Sales Order Confirmation

The module inherits:

```python
sale.order
```

and overrides:

```python
action_confirm()
```

The original Odoo confirmation logic is executed first:

```python
result = super().action_confirm()
```

This is important because it preserves Odoo's standard Sales Order confirmation behavior.

---

## Find Existing Contact History

After confirmation, the module searches for a Contact History for the customer:

```python
history = self.env['contact.history'].search(
    [
        ('partner_id', '=', order.partner_id.id)
    ],
    limit=1
)
```

If one does not exist, it creates one:

```python
history = self.env['contact.history'].create({
    'partner_id': order.partner_id.id,
})
```

---

## Add Sales Order Lines

For every confirmed Sales Order Line, a Contact History Line is created:

```python
self.env['contact.history.line'].create({
    'history_id': history.id,
    'sale_order_id': order.id,
    'product_id': line.product_id.id,
    'description': line.name,
    'unit_price': line.price_unit,
    'product_quantity': line.product_uom_qty,
})
```

Therefore, the flow is:

```text
User confirms Sales Order
          ↓
action_confirm()
          ↓
Odoo confirms the order
          ↓
Find Contact History
          ↓
Does it exist?
      ↙        ↘
    Yes         No
     ↓           ↓
   Use it     Create it
      \         /
       \       /
        ↓     ↓
   Create History Lines
```

---

# User Interface

The module creates a Contact History list view.

It displays:

```text
Partner Name
```

The form view contains three main sections.

### Partner

```text
Partner Name
```

### History

Displays:

```text
Source Document
Product Name
Description
Unit Price
Product Quantity
```

### Invoices

Displays:

```text
Invoice
Invoice Date
Total
Status
```

---

# Sync Contact History Server Action

A server action is defined:

```xml
<record id="action_server_sync_contact_history" model="ir.actions.server">
```

with the name:

```text
Sync Contact History
```

It executes:

```python
action = records.action_sync_history()
```

This allows the synchronization method to be executed from the Contact History form.

After synchronization, the client is reloaded:

```python
return {
    'type': 'ir.actions.client',
    'tag': 'reload',
}
```

This ensures that the newly synchronized data is displayed immediately.

---

# Menu

The module adds:

```text
Contacts
└── Configuration
    └── Contact History
```

The menu uses:

```xml
parent="contacts.res_partner_menu_config"
```

and opens:

```text
action_contact_history
```

---

# Security

The module provides access rights through:

```text
security/ir.model.access.csv
```

The `base.group_user` group receives full CRUD permissions.

```text
Read    ✓
Write   ✓
Create  ✓
Delete  ✓
```

This applies to:

```text
contact.history
contact.history.line
```

---

# Dependencies

The module depends on:

```python
'contacts'
'sale_management'
'account'
```

### Contacts

Provides:

```text
res.partner
```

### Sale Management

Provides:

```text
sale.order
sale.order.line
```

### Account

Provides:

```text
account.move
```

which is used for invoices and refunds.

---

# Manifest

The module manifest contains:

```python
{
    'name': 'Contact History',
    'version': '1.0',
    'category': 'Contacts',
    'author': 'Muhammad Haris',
    'depends': [
        'contacts',
        'sale_management',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/contact_history_views.xml',
    ],
    'installable': True,
    'application': False,
}
```

### `installable`

```python
'installable': True
```

means the module can be installed in Odoo.

### `application`

```python
'application': False
```

means the module is treated as an additional feature rather than a standalone Odoo application.

---

# How It Works

The complete workflow is:

```text
                    CONTACT
                       │
                       ▼
              Contact History
                       │
            ┌──────────┴──────────┐
            │                     │
            ▼                     ▼
      Sales History            Invoices
            │                     │
            ▼                     ▼
   Confirmed Sales Orders   Customer Invoices
            │               & Customer Refunds
            ▼
    Contact History Lines
            │
     ┌──────┼────────┐
     ▼      ▼        ▼
 Product  Price   Quantity
```

There are two ways history data can be populated:

### Method 1 — Automatic

```text
Confirm Sales Order
        ↓
Create/find Contact History
        ↓
Create History Lines
```

### Method 2 — Manual Synchronization

```text
Open Contact History
        ↓
Run "Sync Contact History"
        ↓
Delete old history lines
        ↓
Find confirmed Sales Orders
        ↓
Create History Lines
        ↓
Find invoices/refunds
        ↓
Update invoice_ids
        ↓
Reload page
```

---

# Installation

1. Copy the `contact_history` module into your Odoo custom addons directory.

2. Restart the Odoo server.

3. Activate developer mode if necessary.

4. Go to:

```text
Apps
```

5. Click **Update Apps List**.

6. Search for:

```text
Contact History
```

7. Click **Install**.

---

# Usage

### Create Contact History

Go to:

```text
Contacts → Configuration → Contact History
```

Create a new record and select a partner.

The form will show:

```text
Partner Name
History
Invoices
```

### Synchronize

Use the **Sync Contact History** server action from the Contact History form.

The module will retrieve the partner's:

- Confirmed Sales Orders
- Sales Order Lines
- Customer Invoices
- Customer Refunds

and display them in the history.

---

# Example

Suppose the customer is:

```text
ABC Company
```

and they have confirmed:

```text
SO001
 ├── Laptop × 2
 └── Mouse × 3

SO002
 └── Keyboard × 1
```

After synchronization, Contact History will show:

```text
History
------------------------------------------------
Source     Product       Unit Price    Quantity
SO001      Laptop        1000          2
SO001      Mouse         20            3
SO002      Keyboard      50            1
```

If the customer also has:

```text
INV001
INV002
REF001
```

these will appear in the **Invoices** section.

---