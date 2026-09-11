# Custom Message on Sale Order Email

## Overview

**Custom Message on Email in Sale** is an Odoo module that extends the standard **Sales Order** functionality by allowing users to add a custom message to a sale order.

When the sale order confirmation email is sent, the custom message is automatically included in the email along with the standard order confirmation details.

The module also attaches the standard **Sale Order PDF report** to the confirmation email.

---

## Features

- Adds a **Custom Message** field to the Sale Order form.
- Allows users to enter additional instructions, notes, or messages for the customer.
- Automatically includes the custom message in the sale order confirmation email.
- Displays the customer's name in the email.
- Displays the sale order reference and total order amount.
- Uses the responsible salesperson/company email as the sender.
- Automatically attaches the standard Sale Order PDF report.
- Automatically deletes generated email records after sending.

---

## Module Structure

A typical module structure is:

```text
custom_sale_email/
│
├── __init__.py
├── __manifest__.py
│
├── models/
│   ├── __init__.py
│   └── sale_order.py
│
├── views/
│   └── sale_order_views.xml
│
├── data/
│   └── mail_template.xml
│
└── README.md
```

---

## Main Components

### 1. Custom Message Field

The module inherits the standard `sale.order` model and adds a new Text field:

```python
custom_message = fields.Text(
    string='Custom Message'
)
```

This field allows users to enter any additional message that should be sent to the customer.

---

### 2. Sale Order Form View

The **Custom Message** field is added to the Sale Order form after the existing `note` field.

```xml
<xpath expr="//field[@name='note']" position="after">
    <field name="custom_message"/>
</xpath>
```

This makes the field available directly from the Sale Order interface.

---

### 3. Email Template

The module creates a custom email template for Sale Orders:

```xml
<field name="model_id" ref="sale.model_sale_order"/>
```

The template is linked to the `sale.order` model and contains dynamic information such as:

- Company name
- Customer name
- Sale order reference
- Order total
- Salesperson name
- Custom message

Dynamic Odoo expressions such as:

```xml
<t t-out="object.partner_id.name or ''"/>
```

are used to retrieve information from the current Sale Order.

---

### 4. Custom Message in Email

The custom message is displayed only when the Sale Order contains a message:

```xml
<div t-if="object.custom_message">
```

If the field is empty, the **Custom Message** section will not appear in the email.

This keeps the email clean when no additional message has been provided.

---

### 5. Sale Order PDF Attachment

The standard Odoo Sale Order report is attached to the email using:

```xml
<field name="report_template_ids"
       eval="[(4, ref('sale.action_report_saleorder'))]"/>
```

Therefore, the customer receives the Sale Order PDF along with the confirmation email.

---

## Installation

1. Copy the module into your Odoo custom addons directory.

2. Restart the Odoo server.

3. Enable **Developer Mode**.

4. Go to:

```text
Apps → Update Apps List
```

5. Search for:

```text
Custom message on email in sale
```

6. Click **Install**.

---

## How to Use

### Step 1 — Create a Sale Order

Go to:

```text
Sales → Orders → Quotations
```

Create a new quotation or open an existing Sale Order.

### Step 2 — Add a Custom Message

Enter your required message in the **Custom Message** field.

For example:

```text
Please make sure the order is delivered before Friday.
```

### Step 3 — Confirm the Sale Order

Confirm the quotation to convert it into a Sale Order.

### Step 4 — Send the Confirmation Email

Use the standard Odoo email action to send the order confirmation.

The customer will receive an email containing:

- Customer greeting
- Order reference
- Order total
- Confirmation message
- Salesperson/company details
- Custom Message
- Sale Order PDF attachment

---

## Example Email

```text
Hello John,

Your order SO001 amounting to $1,500.00 has been confirmed.

Thank you for your trust!

Do not hesitate to contact us if you have any questions.

Best regards,
Salesperson Name
Your Company

Custom Message:

Please make sure the order is delivered before Friday.
```

---

## Dependencies

This module depends on:

```python
'depends': [
    'sale_management',
]
```

The `sale_management` module provides the required Sale Order functionality.

---

## Technical Details

### Model Extended

```text
sale.order
```

### Field Added

```text
custom_message
```

**Type:** Text

### View Inherited

```text
sale.view_order_form
```

### Email Template Model

```text
sale.order
```

### Attached Report

```text
sale.action_report_saleorder
```

---

## Configuration

No additional configuration is required.

After installation, the **Custom Message** field becomes available on Sale Orders and the custom email template is loaded automatically.

---

## Compatibility

This module is designed for **Odoo 19** and uses standard Odoo models, XML views, email templates, and QWeb expressions.

---

## License

This module is intended for educational and development purposes.