# Inventory Quantity Access Rights

## Overview

**Inventory Quantity Access Rights** is an Odoo 19 module that controls which users are allowed to edit the **Inventoried Quantity** field in the Inventory adjustment view.

The module introduces a dedicated security group:

> **Can edit inventoried QTY**

Users who belong to this group can edit the inventoried quantity, while other users can only view the value.

---

## Features

- Adds a custom security group for editing inventoried quantities.
- Checks whether the current user belongs to the security group.
- Dynamically controls the readonly status of the **Inventoried Quantity** field.
- Users without permission cannot modify the inventoried quantity.
- Users with permission can edit the quantity directly from the stock quant list view.

---

## Module Structure

```text
custom_permission/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── stock_quant.py
├── security/
│   └── security.xml
└── views/
    └── stock_quant_views.xml
```

---

## Python Implementation

The module inherits the `stock.quant` model and adds a computed Boolean field:

```python
can_edit_inventoried_qty = fields.Boolean(
    compute="_compute_can_edit_inventoried_qty"
)
```

The compute method checks whether the current user belongs to the custom security group:

```python
def _compute_can_edit_inventoried_qty(self):
    can_edit = self.env.user.has_group(
        "custom_permission.group_edit_inventoried_qty"
    )

    for quant in self:
        quant.can_edit_inventoried_qty = can_edit
```

### How it works

`self.env.user.has_group()` returns:

- `True` → User belongs to the group.
- `False` → User does not belong to the group.

The result is stored in `can_edit_inventoried_qty`.

This field is then used by the XML view to determine whether the inventoried quantity field should be editable.

---

## Security Group

The module creates a new user group:

```xml
<record id="group_edit_inventoried_qty" model="res.groups">
    <field name="name">Can edit inventoried QTY</field>
</record>
```

The complete external ID of the group is:

```text
custom_permission.group_edit_inventoried_qty
```

Users who should be allowed to edit inventoried quantities must be added to this group.

---

## View Customization

The module inherits the standard Odoo stock quant tree view:

```xml
<field name="inherit_id" ref="stock.view_stock_quant_tree_editable"/>
```

The permission field is added before `inventory_quantity_auto_apply`:

```xml
<field name="can_edit_inventoried_qty" column_invisible="True"/>
```

The field is hidden from the user because it is only used internally for the permission check.

The inventoried quantity field is then made conditionally readonly:

```xml
<attribute name="readonly">not can_edit_inventoried_qty</attribute>
```

### Result

| User | Can edit Inventoried Quantity? |
|---|---|
| User with **Can edit inventoried QTY** group | ✅ Yes |
| User without the group | ❌ No |

---

## Manifest

The module depends on the Odoo **Stock** module:

```python
"depends": [
    "stock",
],
```

The security and view files are loaded through:

```python
"data": [
    "security/security.xml",
    "views/stock_quant_views.xml",
],
```

Module information:

```text
Name: Inventory Quantity Access Rights
Version: 19.0.1.0.0
License: LGPL-3
Odoo Version: 19.0
```

---

## Installation

1. Place the module inside your Odoo custom addons directory.
2. Restart the Odoo server.
3. Enable **Developer Mode**.
4. Go to:

```text
Apps → Update Apps List
```

5. Search for:

```text
Inventory Quantity Access Rights
```

6. Click **Install**.

---

## Assigning the Permission

After installation:

1. Go to **Settings → Users & Companies → Users**.
2. Open the user who should be allowed to edit inventoried quantities.
3. Assign the **Can edit inventoried QTY** group.
4. Save the user.
5. Open the Inventory adjustment/stock quant view.

Users with the group will be able to edit the inventoried quantity.

---

## Technical Flow

```text
User opens Stock Quant view
          ↓
_compute_can_edit_inventoried_qty()
          ↓
Check user's security group
          ↓
has_group()
     ↙           ↘
  True           False
   ↓               ↓
Editable        Readonly
```

---

## Important Note

The permission is implemented at the **view level** using the computed `can_edit_inventoried_qty` field.

The field itself is computed for each `stock.quant` record based on the current user's group membership. The permission group therefore determines whether the user can edit `inventory_quantity_auto_apply` from this view.

---

## License

This module is licensed under **LGPL-3**.