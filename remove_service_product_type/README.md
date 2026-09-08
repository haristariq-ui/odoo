# Hide Service Product Type

## Overview

This Odoo 19 module removes the **Service** product type option from the Product form view. The Service option is hidden from the product type selection while keeping the other available product types unchanged.

The module uses an Odoo XML view modification together with JavaScript to remove the Service option from the frontend.

## Features

- Removes the **Service** option from the Product Type selection.
- Works on the Odoo Product form view.
- Uses JavaScript to modify the frontend dynamically.
- Automatically handles the product form when it is loaded or updated.
- Does not modify Odoo's core product model.

## Implementation

### XML View

The module inherits the standard `product.template` form view and adds a custom CSS class to the Product Type field:

```xml
<xpath expr="//field[@name='type']" position="attributes">
    <attribute name="class" add="remove_service_product_type"/>
</xpath>
```

This class allows the JavaScript code to identify the Product Type field.

### JavaScript

The JavaScript searches for the Product Type field and looks for the option having:

```html
data-value="service"
```

When found, its corresponding radio item is removed from the page.

A `setInterval()` is used so that the removal also works when Odoo dynamically updates or re-renders the form.

### Module Manifest

The manifest:

- Depends on the `product` module.
- Loads the JavaScript file through `web.assets_backend`.
- Loads the inherited XML view.
- Defines the module as installable but not as a standalone application.

## Module Structure

```text
remove_service_product_type/
├── __init__.py
├── __manifest__.py
├── views/
│   └── product_template_views.xml
└── static/
    └── src/
        └── js/
            └── product_type.js
```

## Result

After installing the module, open a product form and check the **Product Type** field. The **Service** option will no longer be displayed, while the remaining product type options will continue to be available.