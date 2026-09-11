# Odoo Priority-Based Stock Reservation

An Odoo customization that introduces **priority-based stock reservation** for Sales Orders.

The module allows users to assign a stock priority to confirmed Sales Orders. The priority is then transferred to their related Stock Pickings and Stock Moves, allowing Odoo's picking assignment process to consider Sales Order priority when grouping and assigning stock operations.

## Features

- Adds **Stock Priority** to Sales Orders.
- Supports three priority levels:
  - **Highest**
  - **Medium**
  - **Lowest**
- Automatically transfers the Sales Order priority to related Stock Pickings.
- Synchronizes priority changes from Sales Orders to active Pickings.
- Computes Stock Move priority from its related Picking.
- Uses Sales Order priority when creating new Pickings.
- Modifies Picking assignment keys so Sales Orders with different priorities are handled separately.
- Displays priority directly in Sales Order and Stock Picking forms.

## Priority Mapping

The Sales Order uses a human-friendly priority system:

| Sales Order Priority | Stock Priority |
|---|---|
| Highest | Highest |
| Medium | Medium |
| Lowest | Lowest |

Internally, Odoo's stock priority values are:

```text
0 = Normal
1 = Lowest
2 = Medium
3 = Highest
```

The module maps the Sales Order values to these stock priority values using `_get_stock_priority()`.

## How It Works

### 1. Sales Order Priority

A `priority` field is added to `sale.order`.

```python
priority = fields.Selection(
    [
        ('1', 'Highest'),
        ('2', 'Medium'),
        ('3', 'Lowest'),
    ],
    string='Stock Priority',
    default='2',
    required=True,
)
```

The default priority is **Medium**.

### 2. Priority Transfer to Picking

When a Sales Order has confirmed Pickings, its priority is transferred to the related `stock.picking` records.

Only Pickings that are not **Done** or **Cancelled** are updated.

```python
pickings = order.picking_ids.filtered(
    lambda picking: picking.state not in ('done', 'cancel')
)
```

This prevents completed historical Pickings from being modified.

### 3. Priority Synchronization

If the Sales Order priority is changed after confirmation, the module automatically updates the priority of its active Pickings.

This is handled by overriding the `write()` method:

```python
def write(self, vals):
    result = super().write(vals)
    if 'priority' in vals:
        self._update_stock_picking_priority()
    return result
```

### 4. Stock Move Priority

Each Stock Move gets its priority from its related Picking.

```python
def _compute_priority(self):
    for move in self:
        move.priority = move.picking_id.priority or '0'
```

This keeps the priority consistent throughout the stock operation.

### 5. New Picking Priority

When Odoo creates a new Picking from a Stock Move, the module determines the related Sales Order and passes its priority to the new Picking.

The Sales Order can be identified through:

- `sale_line_id.order_id`
- `group_id.sale_id`

This is handled by `_get_sale_order()`.

### 6. Picking Assignment

The `_key_assign_picking()` method is extended to include the Sales Order priority in the Picking assignment key.

```python
return key + (sale_order.priority,)
```

This ensures that stock moves belonging to Sales Orders with different priorities can be separated during Picking assignment rather than being treated as identical based only on the standard Odoo assignment criteria.

## Example

Suppose the following Sales Orders are confirmed:

| Sales Order | Product | Quantity | Priority |
|---|---|---:|---|
| SO001 | Product X | 10 | Highest |
| SO002 | Product X | 10 | Medium |
| SO003 | Product X | 10 | Lowest |

All three orders require the same product.

Their priorities are transferred to their stock operations:

```text
SO001
  ↓
Picking → Highest
  ↓
Stock Moves → Highest

SO002
  ↓
Picking → Medium
  ↓
Stock Moves → Medium

SO003
  ↓
Picking → Lowest
  ↓
Stock Moves → Lowest
```

This allows the stock operation flow to distinguish orders based on their business priority.

## User Interface

The Sales Order priority is displayed on the Sales Order form using a horizontal radio button:

```xml
<field name="priority"
       widget="radio"
       options="{'horizontal': true}"/>
```

The Picking priority is also displayed on the Stock Picking form.

## Technical Details

### Models Extended

- `sale.order`
- `stock.picking`
- `stock.move`

### Main Methods

| Method | Purpose |
|---|---|
| `_get_stock_priority()` | Converts Sales Order priority into Odoo stock priority |
| `_update_stock_picking_priority()` | Updates priority on active Pickings |
| `write()` | Synchronizes Picking priority when Sales Order priority changes |
| `_compute_priority()` | Gets Stock Move priority from Picking |
| `_get_sale_order()` | Finds the related Sales Order |
| `_get_new_picking_values()` | Applies Sales Order priority to newly created Pickings |
| `_key_assign_picking()` | Adds Sales Order priority to Picking assignment logic |

## Important Behavior

- Priority changes only affect Pickings that are not **Done** or **Cancelled**.
- New Pickings inherit priority from their related Sales Order.
- Stock Moves derive their priority from their Picking.
- Sales Orders default to **Medium** priority.
- Existing Odoo stock functionality is preserved through `super()` calls.

## Requirements

- Odoo 19.0
- `sale` module
- `stock` module

## Installation

1. Copy the module into your Odoo custom addons directory.
2. Restart the Odoo server.
3. Activate Developer Mode.
4. Go to **Apps**.
5. Click **Update Apps List**.
6. Search for the module.
7. Click **Install**.

After installation, create or open a Sales Order and select its **Stock Priority** before confirming the order.
