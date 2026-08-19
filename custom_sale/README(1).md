# Custom Sale Order Confirmation

## Overview

This Odoo module customizes the standard **Sale Order** form.

It adds a Boolean field named `confirm_` to `sale.order` and connects it to Odoo's existing **Confirm** and **Cancel** buttons.

The Boolean is not displayed to the user. Instead, it is used as a control field for changing the behavior of other fields in the Sale Order form.

## Features

- Adds a Boolean field `confirm_` to `sale.order`.
- Uses Odoo's built-in **Confirm** button.
- Sets `confirm_ = True` when a quotation is confirmed.
- Uses Odoo's built-in **Cancel** button.
- Sets `confirm_ = False` when the order is cancelled.
- Makes the Customer field readonly when `confirm_` is `True`.
- Makes Payment Terms required when `confirm_` is `True`.
- Makes Order Date invisible when `confirm_` is `True`.
- Makes the selected Order Line column invisible when `confirm_` is `True`.
- Keeps the standard Odoo Sale Order workflow intact.

## Module Structure

```text
custom_sale/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── sale_order.py
└── views/
    └── sale_order_views.xml
```

## Python Model

The module inherits from `sale.order`:

```python
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirm_ = fields.Boolean(
        string='Confirmed',
        default=False
    )

    def action_confirm(self):
        res = super().action_confirm()

        for order in self:
            order.confirm_ = True

        return res

    def action_cancel(self):
        res = super().action_cancel()

        for order in self:
            order.confirm_ = False

        return res
```

### Confirmation Flow

When the user clicks Odoo's standard **Confirm** button:

```text
Confirm button
      ↓
action_confirm()
      ↓
super().action_confirm()
      ↓
confirm_ = True
```

The Boolean then activates the custom view rules.

### Cancellation Flow

When the user clicks Odoo's standard **Cancel** button:

```text
Cancel button
      ↓
action_cancel()
      ↓
super().action_cancel()
      ↓
confirm_ = False
```

The custom view rules are therefore reversed.

## XML View Behavior

The Boolean is included in the form but hidden:

```xml
<xpath expr="//field[@name='partner_id']" position="after">
    <field name="confirm_" invisible="True"/>
</xpath>
```

It is used by other fields as a condition.

### Customer

The Customer becomes readonly after confirmation:

```xml
<field name="partner_id" position="attributes">
    <attribute name="readonly">confirm_</attribute>
</field>
```

### Payment Terms

Payment Terms becomes required after confirmation:

```xml
<field name="payment_term_id" position="attributes">
    <attribute name="required">confirm_</attribute>
</field>
```

### Order Date

Order Date becomes invisible after confirmation:

```xml
<xpath expr="(//field[@name='date_order'])[2]" position="attributes">
    <attribute name="invisible">confirm_</attribute>
</xpath>
```

### Order Line Column

A selected column in the Order Lines is hidden after confirmation:

```xml
<xpath expr="//field[@name='order_line']/list//field[@name='product_uom_qty']"
       position="attributes">
    <attribute name="column_invisible">parent.confirm_</attribute>
</xpath>
```

`parent.confirm_` is used because the field is inside the `sale.order.line` one2many/list view, while `confirm_` belongs to the parent `sale.order`.

## Important Workflow Note

This module does **not** manually change the Sale Order state.

It calls:

```python
super().action_confirm()
```

and:

```python
super().action_cancel()
```

so Odoo's standard workflow remains responsible for changing the actual order state.

The custom Boolean only controls the additional UI behavior.

For example:

```text
Quotation
   │
   │ Confirm
   ▼
Sales Order
confirm_ = True
```

and:

```text
Sales Order / Quotation
   │
   │ Cancel
   ▼
Cancelled
confirm_ = False
```

The Boolean being `False` after cancellation does not convert a cancelled order back into a quotation.

## Installation

1. Place the `custom_sale` module inside your Odoo custom addons directory.
2. Restart the Odoo server.
3. Update the Apps list.
4. Install or upgrade the **Custom Sale** module.
5. Open **Sales → Orders** and create/open a quotation.

## Dependencies

The module depends on the standard Odoo Sales application:

```python
'depends': [
    'sale',
],
```

## Testing Checklist

### Before Confirmation

- [ ] Customer is editable.
- [ ] Payment Terms are not forced to be required by this customization.
- [ ] Order Date is visible.
- [ ] Order-line column is visible.

### After Clicking Confirm

- [ ] Odoo's normal confirmation succeeds.
- [ ] `confirm_` becomes `True`.
- [ ] Customer becomes readonly.
- [ ] Payment Terms becomes invisible.
- [ ] Order Date becomes required.
- [ ] Configured Order Line column becomes invisible.

### After Clicking Cancel

- [ ] Odoo's normal cancellation succeeds.
- [ ] `confirm_` becomes `False`.
- [ ] Customer becomes editable according to the custom rule.
- [ ] Payment Terms returns to its normal behavior.
- [ ] Order Date becomes normal.
- [ ] Configured Order Line column becomes visible again.


## Summary

The main idea of this module is:

```text
Odoo Confirm
      ↓
action_confirm()
      ↓
confirm_ = True
      ↓
Custom UI restrictions activate
```

and:

```text
Odoo Cancel
      ↓
action_cancel()
      ↓
confirm_ = False
      ↓
Custom UI restrictions deactivate
```

The standard Odoo Confirm and Cancel buttons are reused instead of creating separate custom buttons.
