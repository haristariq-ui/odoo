# README — Exchange Price

## Overview

**Exchange Price** is a custom Odoo 19 module that adds an **Exchange Rate** field to pricelist items and uses that rate to convert product prices between currencies.

The exchange rate is applied when the pricelist item's **Compute Price** method is set to **Formula**.

## Features

- Adds an **Exchange Rate** field to `product.pricelist.item`.
- Displays the field in the pricelist item form.
- Shows the field only when **Compute Price = Formula**.
- Supports conversion between:
  - Company currency → foreign currency
  - Foreign currency → company currency
- Uses the manually entered exchange rate for the conversion.
- Keeps the existing Odoo pricelist calculation flow.

## Module Structure

```text
exchange_price/
│
├── __init__.py
├── __manifest__.py
│
├── models/
│   ├── __init__.py
│   └── product_pricelist.py
│
└── views/
    └── product_pricelist.xml
```

## Dependencies

The module depends on:

- `base`
- `product`
- `sale`

These dependencies are defined in `__manifest__.py`.

## Model Customization

The module inherits:

```python
_inherit = "product.pricelist.item"
```

A new field is added:

```python
exchange_rate = fields.Float(
    string="Exchange Rate",
    digits=(16, 4)
)
```

This allows each pricelist item to have its own exchange rate.

## Pricelist Form View

The Exchange Rate field is added after the `currency_id` field:

```xml
<xpath expr="//field[@name='currency_id']" position="after">
    <field
        name="exchange_rate"
        invisible="compute_price != 'formula'"/>
</xpath>
```

Therefore, the field is visible only when the pricelist item uses the **Formula** pricing method.

## Price Conversion Logic

The module overrides:

```python
_compute_base_price()
```

The method first determines:

- The original/base price
- The source currency
- The target currency
- The company currency

The exchange-rate conversion is then performed only when:

```python
src_currency != currency
```

and:

```python
self.compute_price == "formula"
```

and an exchange rate has been entered.

### Company Currency → Foreign Currency

When the product price is in the company currency and the pricelist uses a foreign currency:

```python
if src_currency == company_currency and currency != company_currency:
    price = price * exchange_rate
```

Example:

```text
Product Price = 100 USD
Company Currency = USD
Pricelist Currency = PKR
Exchange Rate = 280

100 × 280 = 28,000 PKR
```

### Foreign Currency → Company Currency

When the product price is in a foreign currency and the pricelist uses the company currency:

```python
elif src_currency != company_currency and currency == company_currency:
    price = price / exchange_rate
```

Example:

```text
Product Price = 28,000 PKR
Company Currency = USD
Exchange Rate = 280

28,000 ÷ 280 = 100 USD
```

## Important Behavior

The exchange rate is applied **only when the source and target currencies are different**.

If both currencies are the same, no conversion is performed.

For example:

```text
USD → USD
```

The original price remains unchanged.

Similarly, the custom exchange rate is not used unless:

```text
Compute Price = Formula
```

## Installation

1. Copy the `exchange_price` module into your Odoo `custom_addons` directory.

2. Restart the Odoo server.

3. Enable **Developer Mode**.

4. Go to:

```text
Apps → Update Apps List
```

5. Search for:

```text
Exchange Price
```

6. Install the module.

## How to Use

1. Open **Sales → Products → Pricelists**.
2. Open or create a pricelist.
3. Add/edit a pricelist item.
4. Set the required currency.
5. Set **Compute Price** to **Formula**.
6. Enter the required **Exchange Rate**.
7. Save the pricelist.
8. Use the pricelist on a quotation or sales order.
9. Verify that the product price is converted using the entered exchange rate.

## Example Test

Assume:

```text
Company Currency: USD
Product Currency: USD
Pricelist Currency: PKR
Product Price: $100
Exchange Rate: 280
Compute Price: Formula
```

Expected result:

```text
100 × 280 = 28,000 PKR
```

For the reverse conversion:

```text
Company Currency: USD
Product Currency: PKR
Pricelist Currency: USD
Product Price: 28,000 PKR
Exchange Rate: 280
```

Expected result:

```text
28,000 ÷ 280 = 100 USD
```
## Author

**Muhammad Haris**

## Version

**1.0**

## Odoo Version

**Odoo 19**