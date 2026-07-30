# Sale Order Category

## Features

- Adds a new **Category** field to Sales Order Lines.
- Automatically retrieves the Product Category when a product is selected.
- Displays the Category as a separate column in the Order Lines section of a Sales Order.
- Improves visibility of product categories without opening product records.

## Module Information

- **Module Name:** Sale Order Category
- **Odoo Version:** 19
- **Dependencies:**
  - sale
## Usage

1. Open **Sales**.
2. Create a new Quotation or open an existing Sales Order.
3. Add a product in the **Order Lines** section.
4. The **Category** field is automatically filled with the selected product's category.

## Technical Details

### Extended Model

- `sale.order.line`

### Added Field

```python
category_id = fields.Many2one(
    "product.category",
    string="Category"
)
```

### Automatic Population

The module uses an `@api.onchange` method to automatically update the Category field whenever the selected product changes.

## Folder Structure

```
sale_order_category/
│
├── models/
│   ├── __init__.py
│   └── sale_order_line.py
│
├── views/
│   └── category_view.xml
│
├── __manifest__.py
├── __init__.py
└── README.md
```
