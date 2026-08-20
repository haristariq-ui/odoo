{
    'name': 'Invoice Balance',
    'version': '1.0',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}