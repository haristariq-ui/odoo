# MRP BOM Label

## Overview
This Odoo 19 module extends the **Manufacturing (MRP)** module to add custom Manufacturing Order information and generate printable BOM labels with barcodes.

## Features
- Adds customer, invoice, delivery, unit, and Sale Order information to Manufacturing Orders.
- Adds fields for dates, Airtable reference, remarks, and completion status.
- Allows users to specify the number of barcode labels to print.
- Adds a **Download** button to print BOM labels.
- Generates a **Code128 barcode** for the related Sale Order.
- Displays product and component information on the label.
- Supports multiple labels for a single Manufacturing Order.
- Uses a custom **101 × 152 mm** portrait paper format.

## Main Components

### Python
Extends `mrp.production` with custom fields and the `action_print_bom_label()` method for generating the report.

### XML Views
Adds the custom fields and **Download** button to the Manufacturing Order form.

### QWeb Report
Creates the BOM label layout containing:
- Manufacturing Order number
- Sale Order barcode and number
- Bill To / Ship To information
- Unit number
- Components
- Product information
- Label numbering

### Dependencies
- `mrp`
- `sale_management`
- `stock`

## Version
**Odoo:** 19.0  
**Module:** MRP BOM Label