# Installed Equipment

## 1. Overview

The **Installed Equipment** module extends Odoo's Inventory and Sales functionality to track equipment products delivered to customers.

The module provides:

- An **Installed Equipment** model.
- An **Installed Equipments** tab on Delivery Orders.
- Automatic creation of Installed Equipment records from Delivery Order Detailed Operations for products marked as equipment.
- An **Is Equipment** field on products.
- A **Rec D Into Inventory** field on lots/serial numbers.
- Automatic copying of the lot/serial **Rec D Into Inventory** value to Installed Equipment.
- Automatic linking of Sale Order, Delivery Order, Customer, and Delivery Date information.
- List and form views for Installed Equipment records.
- A temporary menu for directly accessing Installed Equipment records.

---

## 2. Module Structure

### Python Models

```text
models/
├── __init__.py
├── installed_equipment.py
├── product_template.py
├── stock_lot.py
└── stock_picking.py
```

### XML Views

```text
views/
├── installed_equipment_views.xml
├── product_template_views.xml
├── stock_lot_views.xml
└── stock_picking_new_view.xml
```

### Security

```text
security/
└── ir.model.access.csv
```

---

## 3. Installed Equipment Model

**File:**

```text
models/installed_equipment.py
```

The module introduces the following Odoo model:

```python
_name = "installed.equipment"
```

### Fields

| Field | Type | Purpose |
|---|---|---|
| Product | Many2one | Equipment product |
| Lot/Serial Number | Many2one | Lot or serial number associated with the equipment |
| Sale Order | Many2one | Related Sale Order |
| Delivery Order | Many2one | Related Delivery Order |
| Customer | Many2one | Delivery customer |
| Stock Move Line | Many2one | Related Detailed Operation |
| Installation Date | Date | Equipment installation date |
| Delivery Date | Date | Delivery date |
| Installed at Current Location | Boolean | Indicates whether the equipment is installed at the current location |
| Rec D Into Inventory | Boolean | Stores the inventory-related status |

---

## 4. Lot/Serial Number — Rec D Into Inventory

**File:**

```text
models/stock_lot.py
```

A Boolean field is added to `stock.lot`:

```python
rec_d_into_inventory = fields.Boolean(
    string="Rec D Into Inventory"
)
```

This allows the **Rec D Into Inventory** value to be stored directly against a lot or serial number.

### Lot/Serial Form View

**File:**

```text
views/stock_lot_views.xml
```

The field is inserted after the Product field:

```xml
<xpath expr="//field[@name='product_id']"
       position="after">
    <field name="rec_d_into_inventory"/>
</xpath>
```

---

## 5. Is Equipment on Product

**File:**

```text
models/product_template.py
```

A Boolean field is added to products:

```python
is_equipment = fields.Boolean(
    string="Is Equipment"
)
```

This field determines whether a product should be treated as equipment.

For example:

```text
Product: Laptop
Is Equipment: ✓
```

When this product appears in a Delivery Order's Detailed Operations, it can be used to create an Installed Equipment record.

Products for which **Is Equipment** is disabled are ignored.

### Product View

**File:**

```text
views/product_template_views.xml
```

The **Is Equipment** field is added to the Product form view.

---

## 6. Delivery Order Integration

**File:**

```text
models/stock_picking.py
```

The `stock.picking` model is extended with a relationship to Installed Equipment records:

```python
installed_equipment_ids = fields.One2many(
    "installed.equipment",
    "delivery_order_id",
    string="Installed Equipments",
    compute="_compute_installed_equipment",
    store=True,
)
```

This creates the following relationship:

```text
Delivery Order
      │
      └── Installed Equipments
```

The field is used by the Delivery Order form to display equipment associated with that delivery.

---

## 7. Creating Installed Equipment from Detailed Operations

The module processes the Delivery Order's Detailed Operations:

```python
picking.move_line_ids
```

Each move line is checked to determine whether its product is equipment:

```python
if not move_line.product_id.is_equipment:
    continue
```

The process is therefore:

```text
Detailed Operations
        │
        ├── Product A → Is Equipment ✓
        │                    │
        │                    ▼
        │             Installed Equipment
        │
        ├── Product B → Is Equipment ✗
        │                    │
        │                    ▼
        │                 Ignored
        │
        └── Product C → Is Equipment ✓
                             │
                             ▼
                      Installed Equipment
```

Only products with **Is Equipment** enabled are considered.

---

## 8. Installed Equipment Data

When an equipment product is found in Detailed Operations, an Installed Equipment record is created using information from the Delivery Order and its move line.

The current implementation creates the record using values similar to:

```python
InstalledEquipment.create({
    "delivery_order_id": picking.id,
    "stock_move_line_id": move_line.id,
    "product_id": move_line.product_id.id,
    "lot_id": move_line.lot_id.id,
    "sale_order_id": sale_order.id if sale_order else False,
    "customer_id": picking.partner_id.id,
    "delivery_date": (
        picking.scheduled_date.date()
        if picking.scheduled_date
        else False
    ),
    "rec_d_into_inventory": (
        move_line.lot_id.rec_d_into_inventory
        if move_line.lot_id
        else False
    ),
})
```

### Data Flow

```text
Delivery Order
      │
      ├── Product
      ├── Lot/Serial
      ├── Customer
      ├── Scheduled Date
      └── Sale Order
             │
             ▼
     Installed Equipment
```

---

## 9. Sale Order

The Sale Order is obtained from the Delivery Order:

```python
sale_order = picking.sale_id
```

If a Sale Order exists:

```python
"sale_order_id": sale_order.id
```

is stored on the Installed Equipment record.

If no Sale Order is associated with the Delivery Order:

```python
"sale_order_id": False
```

is stored.

---

## 10. Delivery Date

The Delivery Date is obtained from:

```python
picking.scheduled_date
```

The datetime is converted into a date:

```python
picking.scheduled_date.date()
```

The resulting flow is:

```text
Delivery Order
      │
      ▼
Scheduled Date
      │
      ▼
Convert to Date
      │
      ▼
Installed Equipment
      │
      ▼
Delivery Date
```

---

## 11. Customer

The customer is taken directly from the Delivery Order:

```python
picking.partner_id.id
```

and stored in:

```python
customer_id
```

Therefore:

```text
Delivery Order
      │
      ▼
partner_id
      │
      ▼
Installed Equipment
      │
      ▼
customer_id
```

---

## 12. Rec D Into Inventory

The Installed Equipment record obtains its **Rec D Into Inventory** value from the selected lot/serial number:

```python
move_line.lot_id.rec_d_into_inventory
```

If a lot/serial number exists, its value is copied.

If no lot/serial number is selected, the value is set to:

```python
False
```

The flow is:

```text
Lot/Serial Number
       │
       ▼
Rec D Into Inventory
       │
       ▼
Installed Equipment
```

---

## 13. Lot/Serial Onchange

**File:**

```text
models/installed_equipment.py
```

An onchange is implemented for the Lot/Serial Number field:

```python
@api.onchange("lot_id")
def _onchange_lot_id(self):
    if self.lot_id:
        self.rec_d_into_inventory = self.lot_id.rec_d_into_inventory
    else:
        self.rec_d_into_inventory = False
```

When a user manually selects a Lot/Serial Number on an Installed Equipment record:

```text
Select Lot/Serial
       │
       ▼
_onchange_lot_id()
       │
       ▼
Read Rec D Into Inventory
       │
       ▼
Populate Installed Equipment
```

### Example

```text
Lot/Serial:
LOT001

Rec D Into Inventory:
✓
```

The Installed Equipment record will then show:

```text
Lot/Serial Number:     LOT001
Rec D Into Inventory:  ✓
```

---

## 14. Installed Equipments Tab

**File:**

```text
views/stock_picking_new_view.xml
```

The Delivery Order form inherits:

```xml
stock.view_picking_form
```

A new notebook page is added:

```xml
<page string="installed equipment">
```

The page contains:

```xml
<field name="installed_equipment_ids">
```

and displays the Installed Equipment records associated with the Delivery Order.

### Fields Displayed

The current tab displays:

- Product
- Lot/Serial Number
- Sale Order
- Rec D Into Inventory
- Installed at Current Location
- Installation Date
- Delivery Order

The resulting Delivery Order structure is:

```text
Delivery Order
│
├── Operations
├── Detailed Operations
├── Other existing tabs
└── Installed Equipment
       │
       ├── Product
       ├── Lot/Serial
       ├── Sale Order
       ├── Rec D Into Inventory
       ├── Installation Date
       └── Delivery Order
```

---

## 15. Installed Equipment List View

**File:**

```text
views/installed_equipment_views.xml
```

The list view provides an overview of Installed Equipment records.

### Fields Displayed

```text
Product
Lot/Serial Number
Customer
Sale Order
Delivery Order
Installation Date
Delivery Date
```

This makes it possible to review installed equipment across multiple Delivery Orders.

---

## 16. Installed Equipment Form View

The Installed Equipment form view displays:

```text
Product
Lot/Serial Number
Rec D Into Inventory
Sale Order
Delivery Order
Customer
Installation Date
Delivery Date
Installed at Current Location
Stock Move Line
```

This allows users to open an individual Installed Equipment record and inspect its complete information.

---

## 17. Temporary Installed Equipment Menu

The current XML contains the following action:

```xml
<record id="action_installed_equipment_test" model="ir.actions.act_window">
    <field name="name">Installed Equipments Test</field>
    <field name="res_model">installed.equipment</field>
    <field name="view_mode">list,form</field>
</record>
```

and menu:

```xml
<menuitem
    id="menu_installed_equipment_test"
    name="Installed Equipments Test"
    parent="stock.menu_stock_root"
    action="action_installed_equipment_test"
    sequence="99"/>
```

### Important

This is currently a **temporary/test menu**.

It allows users to open the `installed.equipment` model directly and inspect its records.

For production use, this menu can be renamed or replaced with a permanent menu structure.

---

## 18. Module Dependencies

The module depends on:

```python
'depends': [
    'stock',
    'sale_management',
],
```

Therefore, the following Odoo applications are required:

- **Inventory / Stock**
- **Sales**

---

## 19. Security

The module includes:

```text
security/ir.model.access.csv
```

with access rights for:

```text
installed.equipment
```

The current access rule gives regular internal users:

| Permission | Access |
|---|---|
| Read | ✓ |
| Write | ✓ |
| Create | ✓ |
| Delete | ✓ |

Security permissions should be reviewed before deploying the module to production.

---

## 20. Overall Flow

The complete implementation works conceptually as follows:

```text
                    PRODUCT
                       │
                       ▼
                Is Equipment?
                  /       \
                NO         YES
                │           │
                │           ▼
                │      Delivery Order
                │           │
                │           ▼
                │   Detailed Operations
                │           │
                │           ▼
                │      move_line_ids
                │           │
                │           ▼
                │   Installed Equipment
                │           │
                │     ┌─────┼──────────┐
                │     │     │          │
                │     ▼     ▼          ▼
                │  Product Lot/Serial Sale Order
                │
                │
                └─────────────── Ignored


Lot/Serial
    │
    ▼
Rec D Into Inventory
    │
    ▼
Installed Equipment
```

---

## 21. Task-to-Code Mapping

| Task | Implementation |
|---|---|
| Installed Equipment model | `models/installed_equipment.py` |
| Installed Equipments tab | `views/stock_picking_new_view.xml` |
| Create from Detailed Operations | `_compute_installed_equipment()` in `models/stock_picking.py` |
| Rec D Into Inventory on Lot/Serial | `models/stock_lot.py` |
| Is Equipment on Product | `models/product_template.py` |
| Auto-populate Rec D | `_onchange_lot_id()` and move line logic |
| Sale Order / Delivery / Delivery Date | `models/stock_picking.py` |
| Installed Equipment menu | `views/installed_equipment_views.xml` |
| Installed Equipment list/form | `views/installed_equipment_views.xml` |
| Access rights | `security/ir.model.access.csv` |

---

## 22. Important Implementation Note

The current `stock_picking.py` implementation uses:

```python
@api.depends(...)
def _compute_installed_equipment(self):
```

Inside the compute method, existing Installed Equipment records are removed:

```python
self.installed_equipment_ids.unlink()
```

and new records are then created using:

```python
InstalledEquipment.create(...)
```

### Current Behavior

This means that the `installed_equipment_ids` field is not simply reading existing records. Instead, the current implementation **rebuilds the Installed Equipment records whenever the computed field is recomputed**.

Conceptually:

```text
Compute Trigger
      │
      ▼
Remove Existing Installed Equipment
      │
      ▼
Read Delivery Order Move Lines
      │
      ▼
Find Equipment Products
      │
      ▼
Create Installed Equipment Records
```
