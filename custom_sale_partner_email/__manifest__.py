{
    'name': 'Custom Partner Email',
    'version': '19.0.1.0.0',
    'author': 'Muhammad Haris',
    'license': 'LGPL-3',

    'depends': [
        'sale_management',
        'mail',
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'views/sale_order_views.xml',
        'views/sale_partner_email_wizard_views.xml',
    ],

    'installable': True,
    'application': False,
}