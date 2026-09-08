{
    "name": "Hide Service Product Type",
    "version": "19.0.1.0.0",
    "depends": ["product"],
    "assets": {
        "web.assets_backend": [
            "remove_service_product_type/static/src/js/product_type.js",
        ],
    },
    "data": [
        "views/product_template_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}