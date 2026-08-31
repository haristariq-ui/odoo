{
    'name': 'Contact History',
    'version': '1.0',
    'category': 'Contacts',
    'author': 'Muhammad Haris',
    'depends': [
        'contacts',
        'sale_management',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/contact_history_views.xml',
    ],
    'installable': True,
    'application': False,
}