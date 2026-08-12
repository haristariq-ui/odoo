# Sale Purchase Custom

Custom Odoo 19 module for extending the Sales Order and Customer views
with sales-channel classification, filtering/grouping, customer invoice
access, and additional sales-order information.

## Module Overview

This module extends the standard Odoo Sales functionality.

### Implemented / Covered Features

1.  **Customer Invoices Smart Button**
    -   Adds a smart button on the Customer (`res.partner`) view for
        viewing customer invoices.
    -   The button opens invoices related to the selected customer.
    -   Only customer invoices (`out_invoice`) are displayed.
    -   The action uses a domain based on `partner_id` and `move_type`.
2.  **Sales Channel on Sales Order**
    -   Adds a `Sales Channel` selection field to `sale.order`.
    -   Available options:
        -   Marketing
        -   Trade
        -   Ecommerce
    -   The field is displayed as radio buttons on the Sales Order form.
3.  **Sales Channel Filters**
    -   Adds separate search filters for:
        -   Marketing
        -   Trade
        -   Ecommerce
    -   Each filter uses a domain on the `sales_channel` field.
4.  **Sales Channel Group By**
    -   Adds a `Sales Channel` Group By option to the Sales Order search
        view.
    -   Odoo automatically creates groups for:
        -   Marketing
        -   Trade
        -   Ecommerce
5.  **Additional Sales Order / Sales Order Line Fields**
    -   Existing customizations also add/display:
        -   Custom Order Type on Sales Order
        -   Custom Size on Sales Order Line
        -   Discount Amount on Sales Order Line
        -   Tax Amount on Sales Order Line

## Sales Channel Field

The main field is:

``` python
sales_channel = fields.Selection(
    [
        ('marketing', 'Marketing'),
        ('trade', 'Trade'),
        ('ecommerce', 'Ecommerce'),
    ],
    string='Sales Channel',
)
```

### Selection Value vs Label

Each selection option contains two values:

``` python
('marketing', 'Marketing')
```

-   `marketing` is the internal value stored by Odoo.
-   `Marketing` is the label displayed to the user.

The same pattern is used for Trade and Ecommerce.

## Sales Order Form

The Sales Channel field is displayed using the radio widget:

``` xml
<field name="sales_channel" widget="radio"/>
```

This produces radio buttons on the Sales Order form:

-   Marketing
-   Trade
-   Ecommerce

The field is inserted after the customer field.

## Search Filters

The module adds the following filters:

``` xml
<filter
    name="filter_marketing"
    string="Marketing"
    domain="[('sales_channel', '=', 'marketing')]"/>

<filter
    name="filter_trade"
    string="Trade"
    domain="[('sales_channel', '=', 'trade')]"/>

<filter
    name="filter_ecommerce"
    string="Ecommerce"
    domain="[('sales_channel', '=', 'ecommerce')]"/>
```

### What is a Domain?

A domain is a condition used by Odoo to select records.

For example:

``` python
[('sales_channel', '=', 'marketing')]
```

means:

> Show only Sales Orders whose `sales_channel` value is `marketing`.

The three parts are:

``` text
sales_channel  -> field
=              -> operator
marketing      -> value
```

## Group By

The Sales Order search view also supports:

``` xml
<filter
    name="group_by_sales_channel"
    string="Sales Channel"
    context="{'group_by': 'sales_channel'}"/>
```

This groups Sales Orders according to the value of the `sales_channel`
field.

The result is:

``` text
Marketing
Trade
Ecommerce
```

There is no need to create three separate Group By filters because
Marketing, Trade, and Ecommerce are values of the same field.

## Customer Invoice Smart Button

The customer invoice action uses a domain similar to:

``` python
'domain': [
    ('partner_id', '=', self.id),
    ('move_type', '=', 'out_invoice'),
],
```

This means:

-   `partner_id = self.id` → show invoices belonging to the selected
    customer.
-   `move_type = out_invoice` → show customer invoices rather than
    vendor bills.

The action can also provide default values through context:

``` python
'context': {
    'default_partner_id': self.id,
    'default_move_type': 'out_invoice',
},
```

### Why `res.partner`?

The Customer is represented by the `res.partner` model.

Invoices are related to the customer through the invoice's `partner_id`
field. Therefore, the smart button belongs naturally on the Customer
view and opens the related invoices.

## Sales Order Custom Fields

The Sales Order form customization includes:

``` xml
<field name="sales_channel" widget="radio"/>
```

and:

``` xml
<field name="custom_order_type"/>
```

The Sales Order Line customization displays fields such as:

``` xml
<field name="custom_size"/>
<field name="discount_amount"/>
<field name="tax_amount"/>
```

These are inserted into the existing Odoo Sales Order Line list view
using XPath inheritance.


## XPath

XPath is used to locate an existing element in the parent view.

For example:

``` xml
<xpath expr="//field[@name='partner_id']" position="after">
    <field name="sales_channel" widget="radio"/>
</xpath>
```

This means:

> Find the `partner_id` field and insert `sales_channel` immediately
> after it.

Another example:

``` xml
<xpath expr="//field[@name='payment_term_id']" position="after">
    <field name="custom_order_type"/>
</xpath>
```
## Installation / Upgrade

1.  Place the module inside the configured custom addons directory.
2.  Restart the Odoo server if required.
3.  Open Odoo.
4.  Enable Developer Mode.
5.  Go to **Apps**.
6.  Update the Apps list if the module is not visible.
7.  Install the module.
8.  After code changes, upgrade the module.

## Testing Checklist

### Sales Order

-   [ ] Sales Channel field is visible.
-   [ ] Marketing can be selected.
-   [ ] Trade can be selected.
-   [ ] Ecommerce can be selected.
-   [ ] Sales Channel is saved correctly.

### Filters

-   [ ] Marketing filter shows only Marketing orders.
-   [ ] Trade filter shows only Trade orders.
-   [ ] Ecommerce filter shows only Ecommerce orders.

### Group By

-   [ ] Group By menu contains Sales Channel.
-   [ ] Sales Orders are grouped into Marketing, Trade, and Ecommerce.

### Customer Invoices

-   [ ] Customer view contains the Customer Invoices smart button.
-   [ ] Clicking the button opens invoices for that customer.
-   [ ] Only customer invoices are displayed.

### Additional Fields

-   [ ] Custom Order Type is displayed on the Sales Order.
-   [ ] Custom Size is displayed on Sales Order Lines.
-   [ ] Discount Amount is displayed on Sales Order Lines.
-   [ ] Tax Amount is displayed on Sales Order Lines.

## Key Odoo Concepts Used

This task demonstrates:

-   `fields.Selection`
-   `widget="radio"`
-   Search view inheritance
-   Form view inheritance
-   XPath
-   Search filters
-   Domains
-   Context
-   Group By
-   `ir.actions.act_window`
-   `res.partner`
-   `sale.order`
-   `account.move`
-   Smart buttons
-   Odoo External IDs
-   Odoo view debugging
-   Module upgrade and XML validation

## Troubleshooting


## Conclusion

This customization extends Odoo Sales with a Sales Channel workflow and
improves Sales Order navigation and reporting.

The main workflow is:

``` text
Create Sales Order
        |
        v
Select Sales Channel
        |
   +----+----+-----------+
   |         |           |
Marketing   Trade    Ecommerce
   |         |           |
   +----+----+-----------+
        |
        v
Filter / Group Sales Orders
```

The module also connects customers with their invoices through a smart
button and extends the Sales Order/Sales Order Line views with
additional business information.
