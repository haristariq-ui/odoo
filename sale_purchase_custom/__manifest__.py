{
    'name': 'Sale Purchase Custom',
    'version': '19.0.1.0',
    'depends': [
        'base',
        'sale_management',
        'purchase',
        'account',
        'stock',
    ],
'data': [
        'views/sale_views.xml',
        'views/purchase_views.xml',
        'views/invoice_views.xml',
        'views/stock_views.xml',
        'views/res_partner_views.xml',
    ],


    'installable': True,
}