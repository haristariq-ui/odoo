{
    'name': 'Custom message on email in sale',
    'version': '1.0',
    'depends': [
        'sale_management',
    ],
    'data': [
        'views/sale_order_views.xml',
        'data/mail_template.xml',
    ],
    'installable': True,
    'application': False,
}