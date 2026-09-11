{
    'name': 'school student reporting',
    'version': '1.0',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'views/student_report_views.xml',
    ],

    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}