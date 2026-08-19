# Custom Vendor Selection for Sale Orders

## Overview

This Odoo module extends the **Sale Order Line** and adds a vendor-selection workflow for products.

The main purpose of the module is:

1. Open a vendor-selection wizard directly from a Sale Order Line.
2. Display the selected product's relevant information.
3. Fetch the product's configured vendors.
4. Allow the user to select one vendor.
5. Store the selected vendor on the Sale Order Line.
6. During Sale Order confirmation, use the selected vendor for the purchase procurement flow.
7. Allow Odoo's standard Purchase flow to create/find the Purchase Order for the selected vendor.

---

## Features

### 1. Vendor Data Wizard

A wizard is opened from the Sale Order Line.

The wizard displays product information such as:

- Product
- Internal Reference
- Product Category
- Sales Price

It also contains a **Vendor Lines** section.

Each vendor line displays:

- Vendor
- Vendor Price
- Minimum Quantity
- Delivery Lead Time
- Select Vendor

---

## 2. Get Data Button

The **Get Data** button reads the vendors configured on the selected product.

The vendors are obtained from:

```python
self.product_id.seller_ids
```

For every configured vendor, a wizard line is created containing:

```text
vendor_id
price
min_qty
delay
```

This allows the user to see the available vendors before selecting one.

---

## 3. Vendor Selection

A Boolean field called:

```python
select_vendor
```

was added to the wizard vendor line.

When the user selects a vendor, the selected vendor is written to the Sale Order Line through:

```python
sale_line.custom_vendor_id
```

The Sale Order Line therefore stores the vendor selected by the user.

Example:

```text
Sale Order Line
-----------------------------
Product        : Acoustic Bloc Screens
Purchase Vendor: Ready Mat
```

---

## 4. Custom Vendor Field on Sale Order Line

A custom Many2one field was added:

```python
custom_vendor_id = fields.Many2one(
    "res.partner",
    string="Purchase Vendor",
)
```

This field stores the vendor selected from the wizard.

It is stored on the Sale Order Line so that the selected vendor can later be accessed during the procurement process.

---

## 6. Stock Rule Integration

During procurement, Odoo's `stock.rule` determines which supplier should be used.

The custom implementation checks the Sale Order Line associated with the procurement:

```python
sale_line_id = values.get("sale_line_id")
```

The Sale Order Line is then retrieved:

```python
sale_line = self.env["sale.order.line"].browse(sale_line_id)
```

If a custom vendor was selected, the corresponding supplier information is retrieved using:

```python
product._select_seller(...)
```

The selected supplier is then returned to Odoo's standard purchase procurement flow.

---

## 7. Purchase Order Creation

After the supplier is identified, Odoo's standard purchase flow continues.

The flow is:

```text
Sale Order
    ↓
Sale Order Line
    ↓
Open Vendor Wizard
    ↓
Get Product Vendors
    ↓
Select Vendor
    ↓
custom_vendor_id
    ↓
Sale Order Confirmation
    ↓
Stock Rule
    ↓
Selected Supplier
    ↓
Purchase Procurement
    ↓
Purchase Order / RFQ
```

The module does **not** create a separate "Create Purchase Order" button.

Instead, it works with Odoo's existing procurement and purchase mechanism.

---

## 8. Relationship with Purchase Order

The `sale_purchase` functionality provides the relationship between:

```text
Sale Order Line
        ↕
Purchase Order Line
```

The Purchase Order Line contains the originating Sale Order Line.

This relationship can be used to determine which Purchase Order was generated for a Sale Order Line.

A computed field can therefore display the related Purchase Order on the Sale Order Line.

---

## Main Models Modified

### `sale.order.line`

Customizations include:

```text
custom_vendor_id
purchase_order_id
action_open_vendor_wizard()
```

### `vendor.data.wizard`

Responsible for:

- Displaying product information.
- Displaying vendor information.
- Getting vendor data.
- Handling the selected Sale Order Line.

### `vendor.data.wizard.line`

Responsible for:

- Displaying individual vendors.
- Displaying vendor pricing information.
- Selecting a vendor.

### `stock.rule`

Customized to ensure that the vendor selected on the Sale Order Line is respected during purchase procurement.

---

## User Flow

### Step 1

Create a Sale Order.

### Step 2

Add a product to the Sale Order Line.

### Step 3

Click the **Vendor Data** button.

### Step 4

The Vendor Data Wizard opens.

### Step 5

Click **Get Data**.

The configured vendors for the product are displayed.

### Step 6

Select one vendor.

For example:

```text
Ready Mat
```

The Sale Order Line is updated:

```text
Purchase Vendor: Ready Mat
```

### Step 7

Confirm the Sale Order.

### Step 8

Odoo starts its normal procurement process.

The customization checks the selected vendor.

### Step 9

The selected vendor is passed to the purchase procurement.

### Step 10

Odoo creates/finds the Purchase Order/RFQ for the selected vendor according to its standard purchase flow.

---

## Important Implementation Note

The selected vendor is **not directly used to manually create a Purchase Order**.

Instead, the module passes the selected supplier into Odoo's procurement mechanism.

This keeps the implementation closer to Odoo's standard:

```text
Sale → Stock Rule → Purchase → RFQ/PO
```

rather than manually doing:

```python
self.env["purchase.order"].create(...)
```

This allows the existing Odoo Purchase/Stock logic to continue handling the procurement process.

---

## Technical Summary

The overall implementation can be summarized as:

```text
Product
   │
   ├── Vendor 1
   ├── Vendor 2
   └── Vendor 3
          │
          ▼
Vendor Data Wizard
          │
          ▼
Select Vendor
          │
          ▼
Sale Order Line
custom_vendor_id
          │
          ▼
Sale Order Confirmation
          │
          ▼
supplierinfo
          │
          ▼
stock.rule._get_matching_supplier()
          │
          ▼
Purchase Procurement
          │
          ▼
Purchase Order / RFQ
```

