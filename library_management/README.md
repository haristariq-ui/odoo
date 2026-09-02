# Library Management

An Odoo module for managing library books with **User and Manager security groups** and a simple **book approval workflow**.

## Features

- Create and manage library books.
- Store:
  - Book Name
  - Author
  - Selling Price
  - Cost Price
  - State
- Book states:
  - Draft
  - Approved
- Only **Library Managers** can approve books.
- Cost Price is visible only to **Library Managers**.
- Users have read-only access to books.
- Managers have full CRUD access.

## Module Structure

```text
library_management/
├── __init__.py
├── __manifest__.py
│
├── models/
│   ├── __init__.py
│   └── library_book.py
│
├── security/
│   ├── security.xml
│   └── ir.model.access.csv
│
└── views/
    ├── library_book_views.xml
    └── menu.xml
```

## Model

The module defines the `library.book` model.

| Field | Type | Description |
|---|---|---|
| `name` | Char | Book name, required |
| `author` | Char | Book author |
| `price` | Float | Book price |
| `cost_price` | Float | Cost price, Manager only |
| `state` | Selection | Draft or Approved |

## Security

Two security groups are created:

### Library User

- Can **read** books.
- Cannot create, edit, or delete books.

### Library Manager

- Can **read, create, write, and delete** books.
- Inherits the Library User group.
- Can approve books.
- Can see the `Cost Price` field.

### Approval Security

The `action_approve()` method performs a server-side security check:

```python
if not self.env.user.has_group(
    "library_management.group_library_manager"
):
    raise UserError(
        "Only Library Managers can approve books."
    )
```

This means that even if someone tries to call the method directly, only a Library Manager can approve a book.

## Views

The module provides:

- **List View** – displays books and their basic information.
- **Form View** – displays book details.
- **Approve Button** – available only to Library Managers.
- **Status Bar** – displays the book's current state.

## Menu

```text
Library
└── Books
```

The **Books** menu opens the `library.book` list and form views.

## Dependencies

This module depends only on:

```python
"depends": ["base"]
```

## Installation

1. Copy `library_management` into your custom addons directory.
2. Restart the Odoo server.
3. Enable **Developer Mode**.
4. Go to **Apps**.
5. Update the Apps List.
6. Search for **Library Management**.
7. Install the module.

## Workflow

```text
Library User
     │
     ▼
View Books
     │
     ▼
Library Manager
     │
     ▼
Approve Book
     │
     ▼
Approved
```