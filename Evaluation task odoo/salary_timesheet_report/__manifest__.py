{
    'name': 'Salary Timesheet Report',
    'version': '19.0.1.0.0',
    'author': 'Muhammad Haris',
    'depends': [
        'hr_timesheet',
        'hr_holidays',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/salary_timesheet_wizard_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}