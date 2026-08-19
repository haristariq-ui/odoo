{
    "name": "Sale Order Vendor Wizard",
    "version": "1.0",
    "depends": [
        "sale",
        "sale_stock",
        "sale_purchase",
        "sale_purchase_stock",
        "purchase_stock",
        ],
    "data": [
        'views/sale_order_line_views.xml',
        'views/vendor_data_wizard_views.xml',
        'security/ir.model.access.csv',
    ],
    "installable": True,
    "application": False,
}