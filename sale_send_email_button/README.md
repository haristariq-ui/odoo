# Sale Send by Email Button

An Odoo 19 module that adds a custom **Send by Email** button to Sales Orders. It allows users to open the email composition wizard with a predefined sales order confirmation template and attached sales order report.

## Features

- Adds a **Send by Email** button to the Sales Order form.
- Button is available when the Sales Order is in **Quotation Sent** or **Sales Order** state.
- Opens Odoo's standard email composition wizard.
- Uses a custom **Sales Order Confirmation** email template.
- Automatically uses the customer's email as the recipient.
- Includes the Sales Order reference and total amount in the email body.
- Automatically attaches the Sales Order PDF report.
- Uses the responsible salesperson/company information in the email.
- Automatically deletes the generated email after sending.

## Email Template

The custom email template provides a simple confirmation message containing:

- Customer name
- Sales Order reference
- Total order amount and currency
- Salesperson name
- Company name

The standard Odoo Sales Order report is also attached to the email.

## Technical Implementation

### Python

The `SaleOrder` model is inherited to add the `action_custom_send_email()` method. This method:

1. Loads the custom email template.
2. Loads Odoo's email composition wizard.
3. Passes the required context values to the wizard.
4. Opens the email composer as a popup.
5. Preloads the selected template and Sales Order information.

### XML

The module inherits the standard Sales Order form view and adds the custom **Send by Email** button after Odoo's existing email button.

The email template is defined using `mail.template` and is linked to the `sale.order` model.

## Dependencies

This module depends on:

- `sale`
- `mail`

## Installation

1. Copy the module into your Odoo `custom_addons` directory.
2. Restart the Odoo server.
3. Activate Developer Mode.
4. Go to **Apps** and update the Apps list.
5. Search for **Sale Send by Email Button**.
6. Install the module.

## Usage

1. Open **Sales → Orders**.
2. Open a Sales Order.
3. Confirm the order or send the quotation so that it reaches the required state.
4. Click **Send by Email**.
5. The email composition wizard will open as a popup.
6. Review or modify the email before sending it.
7. The Sales Order PDF will be included as an attachment.

## Module Information

- **Name:** Sale Send by Email Button
- **Version:** 19.0.1.0.0
- **Category:** Sales
- **License:** LGPL-3
- **Odoo Version:** 19