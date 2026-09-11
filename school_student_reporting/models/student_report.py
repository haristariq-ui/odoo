from odoo import fields, models, tools

class SchoolStudentReport(models.Model):
    _name = 'school.student.report'
    _order = 'admission_date desc'
    _auto = False
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
        string='Gender',
        readonly=True,
    )
    class_name = fields.Selection(
        selection=[
            ('9', 'Class 9'),
            ('10', 'Class 10'),
            ('11', 'Class 11'),
            ('12', 'Class 12'),
        ],
        string='Class',
        readonly=True,
    )
    state = fields.Selection(
        selection=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
        ],
        string='Status',
        readonly=True,
    )
    admission_date = fields.Date(
        string='Admission Date',
        readonly=True,
    )
    student_count = fields.Integer(
        string='Students',
        readonly=True,
    )
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    MIN(s.id) AS id,
                    s.gender,
                    s.class_name,
                    s.state,
                    s.admission_date,
                    COUNT(s.id) AS student_count
                FROM school_student s
                GROUP BY
                    s.gender,
                    s.class_name,
                    s.state,
                    s.admission_date
            )
        """)