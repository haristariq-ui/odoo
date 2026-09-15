# Custom Message on Sale Order Email

## Overview

This Odoo module adds a **Custom Message** field to the Sale Order and automatically includes that message in the standard **Sale Order Confirmation Email**.

The main purpose of this module is to allow users to write an additional message for a specific customer/order and have it appear directly in the confirmation email sent from Odoo.

The custom message is displayed only when a message has been entered.

---

## Features

- Adds a **Custom Message** field to `sale.order`.
- Displays the field on the Sale Order form.
- Extends the standard Odoo Sale Order Confirmation Email template.
- Automatically displays the custom message in the email.
- Uses `t-if` so the section is shown only when a custom message exists.
- Keeps the standard Odoo order confirmation content, payment status, and user signature.

---

## Module Structure

A typical module structure is:

```text
custom_message_sale/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── sale_order.py
└── views/
    ├── sale_order_views.xml
    └── mail_template.xml
```

---

## 1. Sale Order Custom Field

The Python model extends the existing `sale.order` model:

```python
from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_message = fields.Text(
        string='Custom Message'
    )
```

The field is a `Text` field, which allows users to enter a longer message.

Because `_inherit = 'sale.order'` is used, no new Sale Order model is created. Instead, the existing Odoo Sale Order model is extended with the new field.

---

## 2. Adding the Field to the Sale Order Form

The field is added after the existing `note` field using an inherited XML view:

```xml
<xpath expr="//field[@name='note']" position="after">
    <field name="custom_message"/>
</xpath>
```

This means the user can enter the custom message directly from the Sale Order form.

For example:

```text
Customer: ABC Company
Order: S00049

Order Lines
-------------------------
Product A       $10.00

Note
-------------------------
Thank you for choosing us.

Custom Message
-------------------------
Please deliver this order before Friday.
```

---

## 3. Modifying the Sale Order Confirmation Email

The module modifies Odoo's existing:

```text
sale.mail_template_sale_confirmation
```

template.

The original template is first made writable by setting its `noupdate` value to `False`.

This allows the module to update the standard Odoo email template during module installation or upgrade.

The template keeps the standard Odoo content such as:

- Customer greeting
- Sale Order number
- Total amount
- Payment status
- Confirmation message
- User signature

The custom section is then added:

```xml
<t t-if="object.custom_message">
    <br/><br/>
    <strong>Custom Message:</strong>
    <br/>
    <t t-out="object.custom_message"/>
</t>
```

---

## 4. How the Custom Message Works

The important part is:

```xml
<t t-if="object.custom_message">
```

Here, `object` represents the current Sale Order.

Therefore:

```text
object.custom_message
```

means:

> Get the custom message entered on this Sale Order.

The `t-if` checks whether the field contains a value.

### If a message exists

For example:

```text
Custom Message:
Please deliver this order before Friday.
```

The email will contain:

```text
Do not hesitate to contact us if you have any questions.

Custom Message:
Please deliver this order before Friday.

--
Mitchell Admin
```

### If no message exists

The entire custom-message section is skipped.

The email will simply contain the normal Odoo confirmation content.

---

## 5. QWeb `t-out`

The custom message is displayed using:

```xml
<t t-out="object.custom_message"/>
```

`t-out` outputs the value of the field into the QWeb email template.

This is preferable to directly inserting the value into HTML because QWeb handles the output safely.

---

## 6. Manifest

The module depends on:

```python
'depends': [
    'sale_management',
],
```

This ensures that the Sale Management functionality and Sale Order models/views are available before this module is loaded.

The XML files are loaded through:

```python
'data': [
    'views/sale_order_views.xml',
    'views/mail_template.xml',
],
```

The module is installable but is not shown as a standalone application:

```python
'installable': True,
'application': False,
```

---

## Workflow

The complete workflow is:

```text
User opens Sale Order
        ↓
Enters Custom Message
        ↓
Confirms Sale Order
        ↓
Odoo sends Sale Order Confirmation Email
        ↓
Email template reads object.custom_message
        ↓
Custom Message is displayed in email
```

---

## Example

Suppose the Sale Order contains:

```text
Order: S00049
Amount: $10.00

Custom Message:
Please make sure the package is delivered during business hours.
```

The confirmation email will contain the normal Odoo confirmation message followed by:

```text
Custom Message:
Please make sure the package is delivered during business hours.
```

If the Custom Message field is empty, this section will not appear.

---

## Installation

1. Place the module inside your Odoo custom addons directory.
2. Restart the Odoo server.
3. Enable **Developer Mode**.
4. Go to **Apps**.
5. Click **Update Apps List**.
6. Search for **Custom message on email in sale**.
7. Install the module.

After installation, open a Sale Order and look for the **Custom Message** field.

---

## Technical Summary

| Component | Purpose |
|---|---|
| `sale.order` | Adds the custom message field |
| `sale_order_views.xml` | Displays the field on the Sale Order form |
| `mail_template.xml` | Modifies the Sale Order confirmation email |
| `t-if` | Displays the message only when it exists |
| `t-out` | Outputs the custom message safely |
| `sale_management` | Module dependency |

## Result

This module provides a simple way to attach **order-specific instructions or messages** to the standard Odoo Sale Order Confirmation Email without creating a completely new email template.