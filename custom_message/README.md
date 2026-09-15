# Custom Message on Sale Order Email

## Overview

This Odoo module adds a **Custom Message** field to Sale Orders and automatically includes that message in the email body when the standard **Sales Order Confirmation** email template is used.

The purpose of this module is to allow sales users to write an order-specific message that is automatically added to the confirmation email without modifying the original Odoo email template.

---

## Features

- Adds a **Custom Message** field to the Sale Order form.
- Displays the field after the existing **Note** field.
- Automatically appends the custom message to the email body.
- Works specifically with Odoo's standard **Sales Order Confirmation** email template.
- Supports multiple lines in the custom message.
- Converts line breaks into HTML `<br/>` tags.
- Escapes user-entered text to prevent unwanted HTML from being rendered.
- Does not affect other email templates or models.

---

## How It Works

The workflow is simple:

1. Open a **Sale Order**.
2. Enter a message in the **Custom Message** field.
3. Confirm/send the Sale Order confirmation email.
4. Odoo opens the standard email composer.
5. The module detects that the standard **Sales Order Confirmation** template is being used.
6. The custom message is retrieved from the Sale Order.
7. The message is appended to the existing email body.
8. The customer receives the standard confirmation email with the custom message included.

### Example

Suppose the Sale Order contains:

**Custom Message:**

```text
Thank you for your order.

Your items will be delivered within 3-5 working days.
```

The email body will contain the existing Odoo confirmation content followed by:

**Custom Message:**

Thank you for your order.

Your items will be delivered within 3-5 working days.

---

## Technical Implementation

### 1. Sale Order Extension

The `sale.order` model is inherited and a new Text field is added:

```python
custom_message = fields.Text(
    string='Custom Message'
)
```

This field stores the message entered by the sales user.

---

### 2. Sale Order Form View

The Sale Order form is inherited and the Custom Message field is placed after the existing `note` field:

```xml
<xpath expr="//field[@name='note']" position="after">
    <field name="custom_message"/>
</xpath>
```

This allows users to enter the message directly from the Sale Order.

---

### 3. Email Composer Customization

The `mail.compose.message` model is inherited and `_compute_body()` is extended.

The module first calls:

```python
super()._compute_body()
```

This ensures that Odoo generates the normal email body first.

The code then checks:

- Whether the standard Sale Order Confirmation template exists.
- Whether the selected template is the standard Sale Order Confirmation template.
- Whether the composer model is `sale.order`.
- Whether exactly one Sale Order is being processed.
- Whether the Sale Order exists.
- Whether a Custom Message has been entered.

Only when all these conditions are satisfied is the custom message added.

---

## Security and HTML Handling

The custom message is processed using:

```python
escape(sale_order.custom_message)
```

This escapes HTML-sensitive characters entered by the user.

For example, text such as:

```html
<b>Hello</b>
```

will not be interpreted as HTML formatting.

Line breaks are converted into HTML line breaks:

```python
.replace('\n', Markup('<br/>'))
```

This ensures that a multi-line message maintains its formatting inside the HTML email.

`Markup` is used to safely construct the HTML section that is appended to the existing email body.

---

## Module Structure

A typical module structure is:

```text
custom_message_on_sale/
│
├── __init__.py
├── __manifest__.py
│
├── models/
│   ├── __init__.py
│   ├── sale_order.py
│   └── mail_compose_message.py
│
└── views/
    └── sale_order_views.xml
```

---

## Dependencies

This module depends on:

```python
'depends': [
    'sale_management',
]
```

The `sale_management` module provides the Sale Order functionality and the standard Sale Order Confirmation email template used by this customization.

---

## Installation

1. Copy the module into your Odoo `custom_addons` directory.
2. Restart the Odoo server.
3. Activate **Developer Mode**.
4. Go to **Apps**.
5. Click **Update Apps List**.
6. Search for **Custom message on email in sale**.
7. Install the module.

---

## Important Behavior

The custom message is **not added to every email**.

It is added only when:

- The email template is `sale.mail_template_sale_confirmation`.
- The email is being composed for a `sale.order`.
- Exactly one Sale Order is being processed.
- The Sale Order contains a Custom Message.

Therefore, other email templates and unrelated email composers continue to work normally.

---

## Manifest

The module is configured as:

```python
{
    'name': 'Custom message on email in sale',
    'version': '1.0',
    'depends': [
        'sale_management',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
}
```

## Summary

This module provides a simple and reusable way to attach **order-specific messages** to standard Sale Order Confirmation emails.

Instead of creating or duplicating the entire Odoo email template, it keeps the standard template intact and dynamically appends the Custom Message when the email composer is generated.