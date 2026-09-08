{
    "name": "Sale Send by Email Button",
    "version": "19.0.1.0.0",
    "category": "Sales",
    "summary": "Adds a Send by Email button to Sales Orders",
    "depends": [
        "sale",
        "mail",
    ],
    "data": [
        "data/sale_email_template.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}