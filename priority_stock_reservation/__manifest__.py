{
    'name': 'Priority-Based Stock Reservation',
    'version': '19.0.1.0.0',
    'author': 'Muhammad Haris',
    'license': 'LGPL-3',
    'depends': [
        'sale_stock',
    ],

    'data': [
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
    ],

    'installable': True,
    'application': False,
}