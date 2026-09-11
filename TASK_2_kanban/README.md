# Kanban Sale Order

## Overview

**Kanban Sale Order** is an Odoo module that extends the Sales application by adding a Kanban-based view for managing and viewing Sale Orders.

The module makes it easier to visually organize Sale Orders using Odoo's Kanban interface.

## Features

- Adds Kanban functionality to Sale Orders.
- Provides a visual representation of Sale Orders.
- Makes it easier to review and organize orders.
- Uses the existing Odoo Sales functionality.
- Lightweight customization with no additional configuration required.

## Installation

1. Copy the module into your Odoo custom addons directory.
2. Restart the Odoo server.
3. Go to **Apps → Update Apps List**.
4. Search for **Kanban Sale Order**.
5. Click **Install**.

## Dependencies

The module depends on the standard Odoo `sale` module:

```python
'depends': [
    'sale',
]
```

## Module Information

| Item | Details |
|---|---|
| Module Name | Kanban Sale Order |
| Version | 1.0 |
| Main Application | Sales |
| Dependency | Sale |
| Type | Odoo Custom Module |
| Installable | Yes |

## Usage

After installation, open the **Sales** application and access the Sale Orders. The Kanban view can be used to visually manage and review Sale Orders.

## License

This module is intended for educational and development purposes.