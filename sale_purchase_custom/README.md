# Custom Sale Order Report – Odoo 19

## Project Overview

This project is an Odoo 19 customization that creates a **custom Sale Order PDF report** using **QWeb**.

The purpose of the customization is to generate a professional Sale Order report that displays the important information from a sales order, including custom fields added to the Sale Order and Sale Order Lines.

The report layout was designed by taking the standard Odoo Sale Order report as a reference and adjusting the alignment, spacing, typography, and table structure.

---

## Technologies Used

- **Odoo 19**
- **Python**
- **XML**
- **QWeb**
- **HTML/CSS**
- **wkhtmltopdf** for PDF report generation

---

## Main Features

### 1. Custom Sale Order PDF Report

A custom QWeb PDF report was created for the `sale.order` model.

The report action uses:

```xml
<field name="model">sale.order</field>
<field name="report_type">qweb-pdf</field>
```

The report is connected to the Sale Order model through:

```xml
<field name="binding_model_id" ref="sale.model_sale_order"/>
<field name="binding_type">report</field>
```

This makes the report available from the Sale Order reporting options.

---

## 2. Sale Order Information

The report displays basic Sale Order information such as:

- Order Number
- Order Date

Example QWeb fields:

```xml
<span t-field="doc.name"/>
<span t-field="doc.date_order"/>
```

---

## 3. Order Information Section

A separate **Order Information** section was created.

It displays:

- Customer
- Sales Channel
- Currency

The custom `sales_channel` field is displayed using:

```xml
<span t-field="doc.sales_channel"/>
```

The customer and currency are displayed using:

```xml
<span t-field="doc.partner_id"/>
<span t-field="doc.currency_id"/>
```

The layout uses Bootstrap/QWeb `row` and `col-*` classes together with CSS styling to control alignment and spacing.

---

## 4. Order Items Table

A custom table was created to display Sale Order Lines.

The table contains:

| Column | Field |
|---|---|
| Product | `line.product_id` |
| Quantity | `line.product_uom_qty` |
| Unit Price | `line.price_unit` |
| Discount | `line.discount_amount` |
| Tax Amount | `line.tax_amount` |
| Subtotal Price | `line.price_subtotal` |

The table was refined to improve:

- Heading alignment
- Numerical value alignment
- Font weight
- Spacing between rows
- Column positioning
- Header border

Numerical columns are right-aligned to make the report easier to read.

---

## 5. Custom Discount and Tax Information

The report displays custom financial information at the bottom.

The summary contains:

- Untaxed Amount
- Total Discount
- Taxes
- Total

Example:

```xml
<span t-field="doc.amount_untaxed"/>
<span t-field="doc.total_discount"/>
<span t-field="doc.amount_tax"/>
<span t-field="doc.amount_total"/>
```

The total amount is displayed in bold.

A horizontal border is placed above the summary to visually separate it from the order lines.

---

## 6. Sale Order Sections and Notes

The report was also updated to support Sale Order sections and notes.

Odoo stores sections and notes as records inside `sale.order.line`, but they are identified using the `display_type` field.

The report checks:

```xml
line.display_type == 'line_section'
```

for sections and:

```xml
line.display_type == 'line_note'
```

for notes.

Normal product lines are handled separately.

The basic QWeb logic is:

```xml
<t t-if="line.display_type == 'line_section'">
    <!-- Display section -->
</t>

<t t-elif="line.display_type == 'line_note'">
    <!-- Display note -->
</t>

<t t-else="">
    <!-- Display normal product line -->
</t>
```

This prevents sections and notes from incorrectly appearing as product lines with empty quantities and prices.

---

## 7. Report Layout Improvements

The report was refined based on the standard Odoo Sale Order report.

The following layout issues were addressed:

### Alignment

Labels and values were aligned consistently.

For example:

- Product text is left-aligned.
- Quantity is left-aligned.
- Unit Price is left-aligned.
- Discount is left-aligned.
- Tax Amount is left-aligned.
- Subtotal is left-aligned.

### Spacing

Spacing was adjusted between:

- Report headings
- Order information
- Order items
- Product rows
- Order totals

### Typography

Important headings and values use bold formatting where appropriate.

For example:

```css
font-weight: bold;
```

### Horizontal separators

Horizontal lines are used to visually separate major sections of the report.

---

## 8. QWeb Report Structure

The report follows the standard Odoo QWeb structure:

```xml
<t t-call="web.html_container">
    <t t-foreach="docs" t-as="doc">
        <t t-call="web.external_layout">

            <div class="page">
                <!-- Report content -->
            </div>

        </t>
    </t>
</t>
```

### `web.html_container`

Provides the HTML container used for the report.

### `docs`

Contains the records for which the report is being generated.

### `doc`

Represents the current Sale Order:

```xml
<t t-foreach="docs" t-as="doc">
```

### `web.external_layout`

Provides the standard Odoo report layout, including company information, logo, header/footer, and page structure.

### `page`

Contains the actual content of the custom report.

---


## 10. Reference Report

The standard Odoo Sale Order report was used as a visual reference.

The custom report was compared against the standard report for:

- Font appearance
- Heading sizes
- Spacing
- Column alignment
- Product-line layout
- Total placement
- Horizontal separators
- Overall page structure

The goal was not to duplicate the standard report exactly, but to follow its professional layout and alignment patterns while displaying the project's custom fields.

---

## 11. Files Involved

The main report customization is contained in the module's XML report file.

Typical structure:

```text
sale_purchase_custom/
│
├── __init__.py
├── __manifest__.py
│
├── models/
│   ├── __init__.py
│   └── sale.py
│
└── sale_report/
    └── sale_order_report.xml
```

---

## 12. Report Action

The report is registered using an `ir.actions.report` record similar to:

```xml
<record id="action_custom_sale_order_report" model="ir.actions.report">
    <field name="name">Custom Sale Order</field>
    <field name="model">sale.order</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">
        sale_purchase_custom.custom_sale_order_report
    </field>
    <field name="report_file">
        sale_purchase_custom.custom_sale_order_report
    </field>
    <field name="binding_model_id" ref="sale.model_sale_order"/>
    <field name="binding_type">report</field>
</record>
```

The important point is that:

```xml
<field name="model">sale.order</field>
```

specifies the Odoo model used by the report, while:

```xml
<field name="binding_model_id" ref="sale.model_sale_order"/>
```

connects the report action to the Sale Order model in Odoo's reporting interface.

---

## 13. Report Generation Flow

The overall process is:

```text
Sale Order
    ↓
Report Action
    ↓
QWeb Template
    ↓
QWeb renders doc / order_line
    ↓
HTML Report
    ↓
wkhtmltopdf
    ↓
PDF Sale Order
```

---

## 14. Key QWeb Concepts Used

### `t-field`

Used to display an Odoo model field:

```xml
<span t-field="doc.name"/>
```

### `t-foreach`

Used to loop through Sale Order Lines:

```xml
<t t-foreach="doc.order_line" t-as="line">
```

### `t-if`

Used to check whether a line is a section:

```xml
<t t-if="line.display_type == 'line_section'">
```

### `t-elif`

Used for notes:

```xml
<t t-elif="line.display_type == 'line_note'">
```

### `t-else`

Used for normal product lines:

```xml
<t t-else="">
```

---

## 15. Current Result

The custom report now provides:

- Standard Odoo external layout
- Sale Order information
- Custom Sales Channel field
- Customer and Currency information
- Custom Order Items table
- Quantity, price, discount, tax, and subtotal
- Order financial summary
- Proper alignment of headings and values
- Improved spacing
- Bold headings and important values
- Section support
- Note support
- PDF generation through QWeb

---

## Conclusion

This project demonstrates how to create and customize a **QWeb PDF report in Odoo 19**.

The implementation covers both the technical side of Odoo reporting and the presentation side, including QWeb templates, report actions, Odoo fields, Sale Order Lines, sections, notes, CSS styling, alignment, spacing, and PDF generation.

The report was developed by studying the standard Odoo Sale Order report and then creating a customized version containing project-specific fields and calculations.
