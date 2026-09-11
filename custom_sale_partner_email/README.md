# Custom Partner Email for Sale Orders

## Overview

**Custom Partner Email** is an Odoo 19 module that extends the standard Sale Order functionality to allow users to send a Sale Order confirmation email to **multiple selected partners**.

The module adds a Many2many partner field to the Sale Order, provides a **Send to Partners** button, and opens a wizard where users can review or change the recipients before sending the email.

Before the email is composed, the module validates that at least one partner has been selected and that all selected partners have valid email addresses.

---

## Features

- Add multiple partners to a Sale Order.
- Display selected partners using Many2many tags.
- Add a **Send to Partners** button to the Sale Order.
- Open a dedicated wizard for selecting email recipients.
- Automatically load the partners selected on the Sale Order into the wizard.
- Validate that at least one recipient is selected.
- Check that all selected partners have an email address.
- Display an error listing partners who do not have an email address.
- Open Odoo's standard email composition window.
- Automatically load the custom email template.
- Send the Sale Order PDF as an attachment.
- Allow users to review the email before sending.

---

## Module Structure

A typical module structure is:

```text
custom_sale_partner_email/
│
├── __init__.py
├── __manifest__.py
│
├── models/
│   ├── __init__.py
│   ├── sale_order.py
│   └── sale_partner_email_wizard.py
│
├── views/
│   ├── sale_order_views.xml
│   └── sale_partner_email_wizard_views.xml
│
├── data/
│   └── email_template.xml
│
├── security/
│   └── ir.model.access.csv
│
└── README.md
```

---

## How It Works

The module follows this flow:

```text
Sale Order
    │
    ▼
Select Partners
    │
    ▼
Click "Send to Partners"
    │
    ▼
Partner Email Wizard
    │
    ▼
Validate Recipients
    │
    ├── No partner → Error
    │
    └── Missing email → Error
    │
    ▼
Open Email Composer
    │
    ▼
Load Email Template
    │
    ▼
Review / Send Email
```

---

## Main Components

### 1. Partner Selection on Sale Order

The `sale.order` model is extended with a Many2many field:

```python
partner_ids = fields.Many2many(
    'res.partner',
    string='Partner IDs',
)
```

This allows multiple contacts to be associated with a Sale Order.

The field is displayed using:

```xml
<field name="partner_ids" widget="many2many_tags"/>
```

This provides a convenient tag-based interface for selecting multiple partners.

---

### 2. Send to Partners Button

A custom button is added to the Sale Order header:

```xml
<button
    name="action_send_to_partners"
    type="object"
    string="Send to Partners"
    class="btn-primary"
    icon="fa-envelope"
/>
```

When the user clicks this button, the Python method `action_send_to_partners()` is executed.

The method opens the custom email wizard and automatically passes the selected Sale Order and partners through the context.

---

### 3. Email Wizard

The module creates a temporary wizard using:

```python
class SalePartnerEmailWizard(models.TransientModel):
    _name = 'sale.partner.email.wizard'
```

The wizard contains two fields:

- **Sale Order** — identifies the Sale Order being emailed.
- **Recipients** — contains the partners who will receive the email.

The Sale Order field is readonly because it is automatically determined from the Sale Order where the button was clicked.

---

## Recipient Validation

Before opening the email composer, the wizard checks whether recipients have been selected:

```python
if not self.partner_ids:
    raise UserError('Please select at least one partner.')
```

It then checks whether every selected partner has an email address.

If one or more partners do not have an email, the system displays their names in an error message:

```text
The following partners do not have an email address:
Partner A, Partner B
```

This prevents the user from continuing with incomplete recipient information.

---

## Email Composition

After successful validation, the module opens Odoo's standard **Email Composer**.

It loads the custom email template using:

```python
template = self.env.ref(
    'custom_sale_partner_email.email_template_custom_sale_order_confirmation'
)
```

The selected partners are passed to the email composer:

```python
'default_partner_ids': self.partner_ids.ids,
```

The Sale Order is also provided as the email's related document.

This means the email template can dynamically access Sale Order information such as:

- Customer name
- Sale Order reference
- Company name
- Order amount
- Salesperson
- Currency

---

## Email Template

The custom email template is based on the `sale.order` model.

The email subject dynamically includes the company name and Sale Order reference:

```text
Company Name - Order confirmation (Ref SO001)
```

The email body contains a simple confirmation message such as:

```text
Hello Customer,

Your order SO001 amounting to $1,000.00 has been confirmed.

Thank you for your trust!

Do not hesitate to contact us if you have any questions.

Best regards,
Salesperson
Company Name
```

The template also attaches the standard Sale Order PDF report:

```xml
<field
    name="report_template_ids"
    eval="[(4, ref('sale.action_report_saleorder'))]"
/>
```

---

## Installation

1. Copy the module into your Odoo custom addons directory.

2. Restart the Odoo server.

3. Enable **Developer Mode** if required.

4. Go to:

```text
Apps → Update Apps List
```

5. Search for:

```text
Custom Partner Email
```

6. Click **Install**.

---

## How to Use

### Step 1 — Open a Sale Order

Go to:

```text
Sales → Orders → Quotations
```

Open an existing quotation or create a new one.

### Step 2 — Select Partners

Use the **Partner IDs** field to select one or more partners.

### Step 3 — Click Send to Partners

Click the **Send to Partners** button in the Sale Order header.

A wizard will appear.

### Step 4 — Review Recipients

The wizard automatically loads the partners selected on the Sale Order.

You can review or modify the recipient list.

### Step 5 — Click Send

The system validates the recipients and opens Odoo's standard email composer.

Review the email and click **Send**.

The selected partners will receive the Sale Order confirmation email with the Sale Order PDF attached.

---

## Dependencies

The module depends on:

```python
'depends': [
    'sale_management',
    'mail',
]
```

### `sale_management`

Provides the Sale Order functionality used by the module.

### `mail`

Provides Odoo's email templates, mail composer, and messaging functionality.

---

## Technical Details

| Component | Value |
|---|---|
| Odoo Version | 19 |
| Module Name | Custom Partner Email |
| Main Model | `sale.order` |
| Wizard Model | `sale.partner.email.wizard` |
| Partner Model | `res.partner` |
| Partner Field | `partner_ids` |
| Wizard Field | `partner_ids` |
| License | LGPL-3 |
| Author | Muhammad Haris |

---

## Important XML and Python References

### Sale Order View

The module inherits:

```text
sale.view_order_form
```

and adds the partner selection field and **Send to Partners** button.

### Email Template

```text
custom_sale_partner_email.email_template_custom_sale_order_confirmation
```

### Wizard View

```text
custom_sale_partner_email.sale_partner_email_wizard_form
```

### Sale Order Report

```text
sale.action_report_saleorder
```

---

## Error Handling

The module handles two important cases:

### No Recipient Selected

If the user removes all recipients from the wizard:

```text
Please select at least one partner.
```

is displayed.

### Partner Has No Email

If a selected partner does not have an email address, the system displays the names of those partners and prevents the email composer from opening.

This helps ensure that emails are only prepared for valid recipients.

---

## License

This module is released under the **LGPL-3** license.