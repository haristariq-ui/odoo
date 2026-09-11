# School Student Reporting

## Overview

**School Student Reporting** is an Odoo 19 module for managing student records and analyzing student data through different reporting views.

The module allows users to create students with information such as name, gender, class, status, and admission date. It also provides a **Student Analysis** section with List, Pivot, and Graph views.

## Features

- Create and manage student records.
- Store student name, gender, class, status, and admission date.
- View students in List and Form views.
- Analyze students using:
  - List View
  - Pivot View
  - Bar Graph
- Filter student analysis by gender, class, status, and admission date.
- Display total student counts.

## Student Model

The main model is:

```text
school.student
```

It contains:

- **Student Name**
- **Gender**
- **Class** — Class 9 to Class 12
- **Status** — Active or Inactive
- **Admission Date**

Students can be accessed from:

```text
School → Students
```

## Student Reporting

The reporting model is:

```text
school.student.report
```

It uses a PostgreSQL SQL View with:

```python
_auto = False
```

The SQL view groups students by **gender, class, status, and admission date** and calculates the number of students using `COUNT()`.

The report is read-only and is used for analysis.

## Reporting Views

### List View

Displays grouped student data and provides a total student count.

### Pivot View

Allows users to analyze student counts by class, gender, and status.

### Graph View

Displays a bar graph showing the number of students in each class.

The reporting section can be accessed through:

```text
School → Reporting → Student Analysis
```

## Installation

1. Copy the module into your Odoo custom addons directory.
2. Restart the Odoo server.
3. Go to **Apps → Update Apps List**.
4. Search for **School Student Reporting**.
5. Click **Install**.

## Dependencies

```python
'depends': [
    'base',
]
```

## Technical Information

| Item | Details |
|---|---|
| Odoo Version | 19 |
| Main Model | `school.student` |
| Report Model | `school.student.report` |
| Report Type | PostgreSQL SQL View |
| Views | List, Pivot, Graph |
| License | LGPL-3 |

## License

This module is released under the **LGPL-3** license.