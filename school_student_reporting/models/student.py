from odoo import fields, models


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'School Student'

    name = fields.Char(
        string='Student Name',
        required=True,
    )

    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
        ],
        string='Gender',
        required=True,
    )

    class_name = fields.Selection(
        [
            ('9', 'Class 9'),
            ('10', 'Class 10'),
            ('11', 'Class 11'),
            ('12', 'Class 12'),
        ],
        string='Class',
        required=True,
    )

    state = fields.Selection(
        [
            ('active', 'Active'),
            ('inactive', 'Inactive'),
        ],
        string='Status',
        default='active',
        required=True,
    )

    admission_date = fields.Date(
        string='Admission Date',
        required=True,
    )