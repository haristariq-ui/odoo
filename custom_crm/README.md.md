# CRM Customer Category

## Overview

This Odoo customization extends the **CRM**, **Contacts**, and **Sales** modules by adding a **Customer Category** field.

The selected customer category is automatically available on CRM Leads and Sales Orders. When a quotation is created from a CRM Lead, the customer's category is automatically populated on the Sales Order.

## Features

- Adds a **Customer Category** field to Contacts.
- Adds **Customer Category** after the Customer field on CRM Leads.
- Adds **Customer Category** after the Customer field on Sales Orders.
- Provides three customer categories:
  - Retail
  - Wholesale
  - Corporate
- Automatically gets the category from the selected customer.
- Automatically populates the customer category on the Sales Order when creating a quotation from a CRM Lead.

## Customer Categories

```text
Retail
Wholesale
Corporate
```

## Module Structure

```text
crm_new/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── crm_lead.py
│   ├── res_partner.py
│   └── sale_order.py
└── views/
    ├── res_partner_views_new.xml
    ├── crm_lead_new.xml
    └── sale_order_new.xml
```

## Field Flow

```text
Contact
   │
   │ customer_category
   ▼
CRM Lead
   │
   │ customer_category
   │
   │ Create Quotation
   ▼
Sales Order
   │
   │ customer_category
   ▼
Retail / Wholesale / Corporate
```

## Implementation

### Contact

The `res.partner` model is extended with a Selection field:

```python
customer_category = fields.Selection(
    [
        ("retail", "Retail"),
        ("wholesale", "Wholesale"),
        ("corporate", "Corporate"),
    ],
    string="Customer Category",
)
```

This is the main field that stores the customer's category.

### CRM Lead

The CRM Lead uses a related field:

```python
customer_category = fields.Selection(
    related="partner_id.customer_category",
    string="Customer Category",
    store=True,
    readonly=False,
)
```

Therefore, when a customer is selected on the CRM Lead, the customer's category is automatically displayed.

### Sales Order

The Sales Order also uses a related field:

```python
customer_category = fields.Selection(
    related="partner_id.customer_category",
    string="Customer Category",
    store=True,
    readonly=False,
)
```

When the customer is selected on the Sales Order, its customer category is automatically displayed.

## CRM → Quotation Flow

1. Open the **CRM** module.
2. Create or open a Lead/Opportunity.
3. Select a customer.
4. The customer's **Customer Category** is automatically displayed.
5. Click **Create Quotation**.
6. Odoo creates a Sales Order for the selected customer.
7. The Sales Order automatically displays the customer's **Customer Category**.

## Example

If the customer has:

```text
Customer: ABC Company
Customer Category: Wholesale
```

The CRM Lead will show:

```text
Customer: ABC Company
Customer Category: Wholesale
```

After clicking **Create Quotation**, the Sales Order will show:

```text
Customer: ABC Company
Customer Category: Wholesale
```

## Dependencies

The module depends on:

```text
account
sale
crm
```

## Installation

1. Place the module inside your Odoo custom addons directory.
2. Restart the Odoo server.
3. Enable Developer Mode.
4. Go to **Apps**.
5. Update the Apps List.
6. Search for **CRM Customer Category**.
7. Install the module.

## Testing

- Create a customer and select a customer category.
- Open CRM and create a Lead/Opportunity for that customer.
- Verify that the category appears automatically.
- Click **Create Quotation**.
- Open the generated Sales Order.
- Verify that the same customer category is displayed.
