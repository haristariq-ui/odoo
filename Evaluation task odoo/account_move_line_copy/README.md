# Salary Timesheet Report

An Odoo 19 module that generates an **Excel salary timesheet report** for active employees within a selected date range.

The report combines:

- Employee total timesheet hours
- Hours grouped by project, task, or activity
- Validated time-off records
- Time-off dates and number of days

The report is generated as an `.xlsx` file using **XlsxWriter**.

---

## Features

- Select a **Start Date** and **End Date**
- Validates that the start date is not after the end date
- Includes all active employees
- Calculates total timesheet hours for each employee
- Groups timesheet hours by:
  - Project
  - Task
  - Activity name
  - Internal work
- Displays validated time-off records
- Shows time-off type, start date, end date, and days
- Generates a formatted Excel report
- Automatically downloads the generated Excel file
- Skips employees who have neither timesheets nor time-off records in the selected period

---

## Module Structure

```text
salary_timesheet_report/
│
├── __init__.py
├── __manifest__.py
│
├── security/
│   └── ir.model.access.csv
│
├── wizard/
│   ├── __init__.py
│   ├── salary_timesheet_wizard.py
│   └── salary_timesheet_wizard_views.xml
│
└── views/
    └── menu.xml
```

---

## Dependencies

This module depends on:

```python
'hr_timesheet',
'hr_holidays',
```

These modules provide the required:

- Employees
- Timesheets
- Time-off records
- Timesheet reporting menu

---

## Wizard

The report uses a transient model:

```python
_name = 'salary.timesheet.wizard'
```

The wizard contains two required fields:

```python
start_date = fields.Date(
    string='Start Date',
    required=True,
)

end_date = fields.Date(
    string='End Date',
    required=True,
)
```

Users select the date range from the wizard before generating the report.

---

## Date Validation

The module prevents an invalid date range where the start date is later than the end date.

```python
@api.constrains('start_date', 'end_date')
def _check_dates(self):
    for record in self:
        if record.start_date > record.end_date:
            raise ValidationError(
                'Start date cannot be greater than end date.'
            )
```

For example:

```text
Start Date: 2026-09-20
End Date:   2026-09-10
```

This will raise a validation error.

---

## Timesheet Data

Timesheets are retrieved from:

```python
account.analytic.line
```

Only timesheets belonging to the selected employee and date range are included.

```python
timesheets = self.env['account.analytic.line'].search([
    ('employee_id', '=', employee.id),
    ('date', '>=', self.start_date),
    ('date', '<=', self.end_date),
], order='date, id')
```

The total employee hours are calculated from `unit_amount`:

```python
total_hours = sum(
    line.unit_amount or 0.0
    for line in timesheets
)
```

---

## Activity-wise Hours

Timesheet hours are grouped into activities.

The activity name is determined in this order:

1. Project name
2. Task name
3. Timesheet description
4. `Internal` if no other information is available

```python
if line.project_id:
    activity_name = line.project_id.name
elif line.task_id:
    activity_name = line.task_id.name
else:
    activity_name = line.name or 'Internal'
```

The hours for the same activity are then added together.

Example:

```text
Employee: Ali

Project A       12 hours
Project B        8 hours
Internal Work    4 hours
-----------------------
Total            24 hours
```

---

## Time-Off Data

Validated time-off records are retrieved from:

```python
hr.leave
```

Only approved/validated leaves overlapping the selected date range are included.

```python
leaves = self.env['hr.leave'].search([
    ('employee_id', '=', employee.id),
    ('state', '=', 'validate'),
    ('date_from', '<=', end_datetime),
    ('date_to', '>=', start_datetime),
], order='date_from')
```

The report displays:

- Time-off type
- Start date
- End date
- Number of days

Time-off rows are highlighted separately in the Excel report.

---

## Excel Report

The report is generated using:

```python
import xlsxwriter
```

The workbook is created in memory:

```python
output = io.BytesIO()

workbook = xlsxwriter.Workbook(
    output,
    {'in_memory': True}
)
```

The worksheet is named:

```text
CW Salary Report
```

The report contains the following columns:

| Column | Description |
|---|---|
| ID | Employee report number |
| Employee | Employee name |
| Start Date | Time-off start date |
| End Date | Time-off end date |
| Hours | Timesheet hours |
| Days | Time-off days |

---

## Report Layout

The generated report follows this structure:

```text
CW Salary Report From 2026-09-01 To 2026-09-30

ID | Employee | Start Date | End Date | Hours | Days
------------------------------------------------------
1  | Employee A                         | 160   |
   | Project A                          | 100   |
   | Project B                          | 60    |
   | Annual Leave | 2026-09-15 | 2026-09-17 |   | 3
------------------------------------------------------

2  | Employee B                         | 145   |
   | Project C                          | 120   |
   | Internal                           | 25    |
   | Sick Leave   | 2026-09-20 | 2026-09-20 |   | 1
------------------------------------------------------
```

Employees without either timesheet or validated time-off records are not included.

---

## Excel Formatting

Different formats are used for different types of rows.

### Employee Rows

Employee names and total hours are displayed in bold.

### Activity Rows

Activity names and hours use normal formatting.

### Time-Off Rows

Time-off rows are highlighted with a light green background to distinguish them from timesheet data.

The worksheet also includes:

- Adjusted column widths
- Frozen panes
- Number formatting for hours and days
- A report title
- Employee numbering

---

## File Generation

After generating the workbook, it is converted to Base64:

```python
file_data = base64.b64encode(
    output.read()
)
```

The Excel file is then stored as an Odoo attachment:

```python
attachment = self.env['ir.attachment'].create({
    'name': 'CW_Salary_Report_%s_%s.xlsx' % (
        self.start_date,
        self.end_date,
    ),
    'type': 'binary',
    'datas': file_data,
    'res_model': self._name,
    'res_id': self.id,
})
```

Finally, the user is redirected to the generated file for download.

---

## User Interface

The wizard provides two date fields:

```text
+-----------------------------+
|      Salary Timesheet       |
|                             |
| Start Date:  [  Date     ]  |
| End Date:    [  Date     ]  |
|                             |
|       [ Generate ] [Cancel] |
+-----------------------------+
```

The wizard opens as a popup because the action uses:

```xml
<field name="target">new</field>
```

---

## Menu

A **Salary Timesheet** menu is added under the Timesheets Reports menu:

```xml
<menuitem
    id="menu_salary_timesheet"
    name="Salary Timesheet"
    parent="hr_timesheet.menu_timesheets_reports"
    action="action_salary_timesheet_wizard"
    sequence="20"
/>
```

Users can access the wizard from the Timesheets reporting section.

---

## Installation

1. Copy the module into your Odoo custom addons directory.

2. Make sure the module directory is included in Odoo's addons path.

3. Restart the Odoo server.

4. Activate developer mode if necessary.

5. Go to:

```text
Apps → Update Apps List
```

6. Search for:

```text
Salary Timesheet Report
```

7. Click **Install**.

---

## Usage

After installation:

1. Open the **Timesheets** application.
2. Go to the **Reports** section.
3. Select **Salary Timesheet**.
4. Enter the **Start Date**.
5. Enter the **End Date**.
6. Click **Generate**.
7. The Excel report will be generated and downloaded.

---

## Technical Details

| Item | Value |
|---|---|
| Odoo Version | 19.0 |
| Module Name | Salary Timesheet Report |
| Model | `salary.timesheet.wizard` |
| Model Type | TransientModel |
| Excel Library | XlsxWriter |
| Main Timesheet Model | `account.analytic.line` |
| Employee Model | `hr.employee` |
| Time-Off Model | `hr.leave` |
| License | LGPL-3 |

---

## Manifest

```python
{
    'name': 'Salary Timesheet Report',
    'version': '19.0.1.0.0',
    'author': 'Muhammad Haris',
    'depends': [
        'hr_timesheet',
        'hr_holidays',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/salary_timesheet_wizard_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
```

## License

This module is licensed under the **LGPL-3** license.