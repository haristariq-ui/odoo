# Pricelist PDF and Excel Report

## Overview

This is a custom **Odoo module** that adds PDF and Excel reporting functionality to the standard **Product Pricelist** model.

The module adds two reporting options:

1. **PDF Report** — Generates a formatted PDF containing the pricelist information and products.
2. **Excel Report** — Generates an `.xlsx` file containing the pricelist information and product prices.

The module extends Odoo's existing `product.pricelist` model instead of creating a new model.

---

## Features

### PDF Report

The PDF report displays:

- Pricelist name
- Currency
- Product Code
- Product Description
- Unit Price
- Currency used for the unit price

Example structure:

```text
Pricelist Name
Currency: USD

---------------------------------------------------------
Product Code | Product Description | Unit Price (USD)
---------------------------------------------------------
P001         | Product A           | 100.00
P002         | Product B           | 250.00
---------------------------------------------------------
```

### Excel Report

The Excel report contains:

- Pricelist name
- Currency
- Product Code
- Product Description
- Unit Price

The Excel file is generated dynamically and downloaded by the user.

---

# Module Structure

A typical module structure is:

```text
custom_pricelist_report/
│
├── __init__.py
├── __manifest__.py
│
├── models/
│   ├── __init__.py
│   └── pricelist.py
│
└── report/
    ├── pricelist_report.xml
    └── pricelist_report_template.xml
```

---

# 1. Python Model

The Python code extends the existing Odoo `product.pricelist` model.

```python
class ProductPricelist(models.Model):
    _inherit = "product.pricelist"
```

This means:

> "Take Odoo's existing Product Pricelist model and add new functionality to it."

No new database model is created.

---

# 2. PDF Report

The following method is responsible for generating the PDF:

```python
def action_print_pricelist_pdf(self):
    self.ensure_one()
    return self.env.ref(
        "custom_pricelist_report.action_report_pricelist_pdf"
    ).report_action(self)
```

## What does `ensure_one()` do?

```python
self.ensure_one()
```

It makes sure that the user selected **only one pricelist**.

For example:

```text
Selected Pricelist:
        ↓
My Pricelist
        ↓
Generate PDF
```

The report is designed to work with one pricelist at a time.

---

## How the PDF action works

This line:

```python
self.env.ref(
    "custom_pricelist_report.action_report_pricelist_pdf"
)
```

finds the XML report action using its external ID.

The external ID is:

```text
custom_pricelist_report.action_report_pricelist_pdf
```

Then:

```python
.report_action(self)
```

tells Odoo:

> Generate this report using the current pricelist record.

---

# 3. Excel Report

The Excel functionality is implemented in:

```python
def action_export_pricelist_excel(self):
```

The process is:

```text
User clicks Excel
       ↓
Odoo calls action_export_pricelist_excel()
       ↓
Create Excel file in memory
       ↓
Create worksheet
       ↓
Add pricelist information
       ↓
Add product information
       ↓
Save Excel data
       ↓
Create Odoo attachment
       ↓
Return download URL
       ↓
Browser downloads .xlsx file
```

---

# 4. Creating the Excel File

The code uses the `xlsxwriter` Python library.

```python
import xlsxwriter
```

A memory buffer is created:

```python
output = io.BytesIO()
```

This creates a temporary place in memory where the Excel file can be built.

Then:

```python
workbook = xlsxwriter.Workbook(output, {
    "in_memory": True,
})
```

creates the Excel workbook.

The important point is:

> The Excel file is created in memory first. It is not immediately saved as a physical file on the server.

---

# 5. Creating the Worksheet

```python
worksheet = workbook.add_worksheet("Pricelist")
```

This creates an Excel sheet named:

```text
Pricelist
```

So the Excel file looks approximately like:

```text
Pricelist.xlsx
    |
    └── Pricelist
```

---

# 6. Excel Formatting

Three main formatting objects are created.

### Title Format

```python
title_format = workbook.add_format({
    "bold": True,
    "font_size": 14,
})
```

This makes the text:

- Bold
- 14px font size

---

### Header Format

```python
header_format = workbook.add_format({
    "bold": True,
    "border": 1,
})
```

This creates:

- Bold text
- Border around the cell

It is used for headings such as:

```text
Currency
Product Code
Product Description
Unit Price
```

---

### Normal Cell Format

```python
cell_format = workbook.add_format({
    "border": 1,
})
```

This adds a border to normal cells.

---

### Price Format

```python
price_format = workbook.add_format({
    "border": 1,
    "num_format": "0.00",
})
```

This is used for prices.

For example:

```text
100
```

will be displayed as:

```text
100.00
```

---

# 7. Excel Column Widths

```python
worksheet.set_column("A:A", 20)
worksheet.set_column("B:B", 35)
worksheet.set_column("C:C", 20)
```

These lines control the width of the Excel columns.

```text
A → 20
B → 35
C → 20
```

The columns represent:

```text
A = Product Code
B = Product Description
C = Unit Price
```

---

# 8. Understanding A1, A2, B2

Excel uses a cell-address system.

For example:

```text
A1
```

means:

```text
Column A
Row 1
```

Similarly:

```text
B2
```

means:

```text
Column B
Row 2
```

The Excel sheet can be visualized like this:

```text
        A                 B                    C
    ------------------------------------------------
1   Pricelist Name
    ------------------------------------------------
2   Currency           USD
    ------------------------------------------------
3
    ------------------------------------------------
4   Product Code       Product Description     Unit Price
    ------------------------------------------------
5   P001               Product A               100.00
6   P002               Product B               200.00
```

---

# 9. Writing Pricelist Information

The pricelist name is written to cell `A1`:

```python
worksheet.write("A1", self.name, title_format)
```

`self.name` is the current pricelist's name.

For example:

```text
self.name = "Retail Pricelist"
```

Then Excel will contain:

```text
A1 → Retail Pricelist
```

---

## Currency

```python
worksheet.write("A2", "Currency", header_format)
```

This writes:

```text
A2 → Currency
```

Then:

```python
worksheet.write(
    "B2",
    self.currency_id.name or "",
    cell_format,
)
```

writes the currency.

For example:

```text
B2 → USD
```

So:

```text
A2 = Currency
B2 = USD
```

---

# 10. Table Headers

The variable:

```python
row = 4
```

is used because Python counts rows starting from `0`.

So:

```text
Python row 4
```

represents:

```text
Excel row 5
```

The headers are written using:

```python
worksheet.write(row, 0, "Product Code", header_format)
worksheet.write(row, 1, "Product Description", header_format)
worksheet.write(
    row,
    2,
    "Unit Price (%s)" % self.currency_id.name,
    header_format,
)
```

The numbers mean:

```text
0 → Column A
1 → Column B
2 → Column C
```

Therefore:

```text
Column 0 → A
Column 1 → B
Column 2 → C
```

---

# 11. Reading Pricelist Lines

The code then loops through the pricelist items:

```python
for line in self.item_ids:
```

`self.item_ids` contains the pricing rules/items belonging to the current pricelist.

For example:

```text
Pricelist
   |
   ├── Product A → $100
   ├── Product B → $200
   └── Product C → $300
```

The loop processes each item one by one.

---

# 12. Checking for a Product

```python
if not line.product_tmpl_id:
    continue
```

This means:

> If this pricelist line does not have a product template, skip it.

`continue` means:

> Don't process this line. Move to the next line.

---

# 13. Getting the Product

```python
product = line.product_tmpl_id
```

Now the product template is stored in:

```text
product
```

Instead of repeatedly writing:

```python
line.product_tmpl_id
```

the code can simply use:

```python
product
```

---

# 14. Product Code

```python
product.product_variant_id.default_code
```

This gets the product's internal reference/code.

For example:

```text
P001
```

The code:

```python
worksheet.write(
    row,
    0,
    product.product_variant_id.default_code or "",
    cell_format,
)
```

writes it into column A.

---

# 15. Product Name

```python
product.name
```

gets the product name.

For example:

```text
Laptop
```

This is written into column B:

```python
worksheet.write(
    row,
    1,
    product.name or "",
    cell_format,
)
```

---

# 16. Product Price

```python
line.fixed_price
```

gets the fixed price configured on the pricelist line.

For example:

```text
250.00
```

It is written into column C:

```python
worksheet.write_number(
    row,
    2,
    line.fixed_price,
    price_format,
)
```

---

# 17. Moving to the Next Excel Row

After writing one product:

```python
row += 1
```

This means:

> Move to the next row for the next product.

For example:

```text
Product A → row 5
Product B → row 6
Product C → row 7
```

---

# 18. Closing the Workbook

After all products have been processed:

```python
workbook.close()
```

This finishes the Excel file.

Then:

```python
output.seek(0)
```

moves the pointer back to the beginning of the generated file.

Then:

```python
file_data = output.read()
```

reads the complete Excel file.

Finally:

```python
output.close()
```

closes the temporary memory buffer.

---

# 19. Creating an Odoo Attachment

The Excel data is stored in Odoo as an attachment:

```python
attachment = self.env["ir.attachment"].create({
```

The attachment name is:

```python
"name": "%s.xlsx" % self.name,
```

For example:

```text
Retail Pricelist.xlsx
```

The file type is:

```python
"type": "binary"
```

The Excel data is encoded using Base64:

```python
"datas": base64.b64encode(file_data)
```

Odoo commonly stores binary file data in Base64 format.

---

# 20. Downloading the Excel File

The method returns:

```python
return {
    "type": "ir.actions.act_url",
    "url": "/web/content/%s?download=true" % attachment.id,
    "target": "self",
}
```

This tells Odoo to open the attachment URL and download the file.

The complete flow is:

```text
Generate Excel
      ↓
Store Excel in memory
      ↓
Create ir.attachment
      ↓
Get attachment ID
      ↓
Create download URL
      ↓
Browser downloads Excel
```

---

# 21. PDF Report XML Action

The PDF report is registered using:

```xml
<record id="action_report_pricelist_pdf" model="ir.actions.report">
```

This creates an Odoo report action.

Important fields include:

```xml
<field name="model">product.pricelist</field>
```

This tells Odoo:

> This report is for the Product Pricelist model.

---

## Report Type

```xml
<field name="report_type">qweb-pdf</field>
```

This means:

> Use a QWeb template and generate a PDF.

---

## Report Template

```xml
<field name="report_name">
    custom_pricelist_report.pricelist_report_template
</field>
```

This points to the QWeb template.

The template ID is:

```text
pricelist_report_template
```

inside the module:

```text
custom_pricelist_report
```

---

# 22. Binding the PDF Report

```xml
<field name="binding_model_id"
       ref="product.model_product_pricelist"/>
```

This connects the report to the Product Pricelist model.

```xml
<field name="binding_type">report</field>
```

This tells Odoo that it is a report action.

As a result, the report can appear in the Product Pricelist's reporting/print actions.

---

# 23. Excel Server Action

Excel uses a server action:

```xml
<record id="action_export_pricelist_excel_print"
        model="ir.actions.server">
```

The action is connected to:

```xml
<field name="model_id"
       ref="product.model_product_pricelist"/>
```

The important part is:

```xml
<field name="code">
    action = record.action_export_pricelist_excel()
</field>
```

This means:

> When the user runs the Excel action, call the Python method `action_export_pricelist_excel()`.

The flow is:

```text
User clicks Excel
       ↓
Server Action
       ↓
record.action_export_pricelist_excel()
       ↓
Python generates Excel
       ↓
Download Excel
```

---

# 24. QWeb PDF Template

The PDF template starts with:

```xml
<template id="pricelist_report_template">
```

This defines the HTML/QWeb template used to generate the PDF.

---

## `docs`

The report receives the records through:

```xml
<t t-foreach="docs" t-as="doc">
```

Here:

```text
docs = records sent to the report
doc  = one record from docs
```

Because the report is for `product.pricelist`:

```text
doc = one Product Pricelist
```

---

# 25. External Layout

```xml
<t t-call="web.external_layout">
```

This uses Odoo's standard external report layout.

It can provide things such as:

- Company information
- Header
- Footer
- Page structure

---

# 26. Pricelist Name

```xml
<span t-field="doc.name"/>
```

Displays the pricelist name.

For example:

```text
Retail Pricelist
```

---

# 27. Currency

```xml
<span t-field="doc.currency_id"/>
```

Displays the currency of the pricelist.

For example:

```text
USD
```

---

# 28. PDF Table

The report contains a table:

```xml
<table class="table table-bordered table-sm">
```

The table has three columns:

```text
Product Code
Product Description
Unit Price
```

The widths are:

```text
20% → Product Code
55% → Product Description
25% → Unit Price
```

Total:

```text
20% + 55% + 25% = 100%
```

---

# 29. Looping Through Products in PDF

The template loops through the pricelist items:

```xml
<t t-foreach="doc.item_ids" t-as="line">
```

Then checks:

```xml
<t t-if="line.product_tmpl_id">
```

This means:

> Only display lines that have a product template.

Then the product information is displayed.

---

# 30. Product Code in PDF

```xml
<span t-esc="
    line.product_tmpl_id.product_variant_id.default_code or ''
"/>
```

This displays the product's internal reference.

Example:

```text
P001
```

---

# 31. Product Description in PDF

```xml
<span t-field="line.product_tmpl_id.name"/>
```

This displays the product name.

Example:

```text
Laptop
```

---

# 32. Unit Price in PDF

```xml
<span t-esc="'%.2f' % line.fixed_price"/>
```

This formats the price to exactly two decimal places.

For example:

```text
100
```

becomes:

```text
100.00
```

And:

```text
25.5
```

becomes:

```text
25.50
```

---

# 33. Manifest File

The `__manifest__.py` file contains:

```python
{
    "name": "Pricelist PDF and Excel Report",
```

This is the module's name displayed in Odoo.

---

## Version

```python
"version": "1.0.0",
```

This is the module version.

---

## Category

```python
"category": "Sales",
```

The module belongs to the Sales category.

---

## Author

```python
"author": "Muhammad Haris",
```

The module author.

---

## License

```python
"license": "LGPL-3",
```

The module uses the LGPL-3 license.

---

# 34. Module Dependency

```python
"depends": [
    "sale",
],
```

This means the module depends on Odoo's Sales module.

The `sale` module provides the required Product Pricelist functionality.

Therefore:

```text
Sales Module
      ↓
Product Pricelist
      ↓
Custom Pricelist Report
```

---

# 35. Data Files

The manifest loads:

```python
"data": [
    "report/pricelist_report_template.xml",
    "report/pricelist_report.xml",
],
```

These XML files must be loaded by Odoo.

### `pricelist_report_template.xml`

Contains the actual QWeb PDF template.

### `pricelist_report.xml`

Contains the PDF report action and Excel server action.

---

# 36. Installation

Copy the module into your Odoo custom addons directory:

```text
custom_addons/
└── custom_pricelist_report/
```

Make sure the module contains:

```text
__init__.py
__manifest__.py
models/
report/
```

Then restart the Odoo server.

Update the Apps list:

```text
Apps
   ↓
Update Apps List
```

Search for:

```text
Pricelist PDF and Excel Report
```

Install the module.

---

# 37. Complete Flow

## PDF Flow

```text
Product Pricelist
       ↓
Print / PDF
       ↓
action_report_pricelist_pdf
       ↓
QWeb Template
       ↓
pricelist_report_template
       ↓
PDF
```

## Excel Flow

```text
Product Pricelist
       ↓
Excel
       ↓
Server Action
       ↓
action_export_pricelist_excel()
       ↓
Create Excel in Memory
       ↓
Add Pricelist Information
       ↓
Add Product Information
       ↓
Create ir.attachment
       ↓
Download URL
       ↓
Excel File
```

---

# 38. Important Odoo Concepts Used

| Concept | Purpose |
|---|---|
| `_inherit` | Extends an existing Odoo model |
| `ensure_one()` | Makes sure only one record is selected |
| `env.ref()` | Finds an Odoo record using its XML ID |
| `report_action()` | Generates a report |
| QWeb | Odoo's XML/HTML reporting system |
| `ir.actions.report` | Defines a report |
| `ir.actions.server` | Defines a server-side action |
| `ir.attachment` | Stores files in Odoo |
| `BytesIO` | Creates an in-memory file |
| `xlsxwriter` | Creates Excel files |
| `base64` | Encodes binary file data |
| `t-foreach` | Loops through records in QWeb |
| `t-if` | Adds a condition in QWeb |
| `t-field` | Displays an Odoo field |
| `t-esc` | Displays escaped/calculated values |

---

# 39. Final Result

After installing the module, the Product Pricelist can be used to generate:

```text
                    Product Pricelist
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
          PDF Report                Excel Report
             │                           │
             ▼                           ▼
       QWeb Template              XlsxWriter
             │                           │
             ▼                           ▼
          PDF File                  .xlsx File
```

The module therefore provides a simple way to export Odoo pricelist data into both **PDF** and **Excel** formats.