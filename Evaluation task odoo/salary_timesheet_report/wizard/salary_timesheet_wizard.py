from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import io
import xlsxwriter

class SalaryTimesheetWizard(models.TransientModel):
    _name = 'salary.timesheet.wizard'

    start_date = fields.Date(
        string='Start Date',
        required=True,
    )
    end_date = fields.Date(
        string='End Date',
        required=True,
    )
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date > record.end_date:
                raise ValidationError(
                    'Start date cannot be greater than end date.'
                )

    def action_generate_report(self):
        self.ensure_one()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(
            output,
            {'in_memory': True}
        )
        worksheet = workbook.add_worksheet('CW Salary Report')
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'left',
            'valign': 'vcenter',
        })
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#D3D3D3',
            'border': 0,
            'align': 'left',
            'valign': 'vcenter',
        })
        employee_format = workbook.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'vcenter',
        })

        employee_hours_format = workbook.add_format({
            'bold': True,
            'align': 'right',
            'num_format': '0',
        })

        activity_format = workbook.add_format({
            'align': 'left',
        })

        activity_hours_format = workbook.add_format({
            'align': 'right',
            'num_format': '0',
        })

        timeoff_format = workbook.add_format({
            'bold': True,
            'bg_color': '#C6EFCE',
            'align': 'left',
            'valign': 'vcenter',
        })

        timeoff_date_format = workbook.add_format({
            'bg_color': '#C6EFCE',
            'num_format': 'yyyy-mm-dd',
            'align': 'left',
        })

        timeoff_days_format = workbook.add_format({
            'bg_color': '#C6EFCE',
            'num_format': '0',
            'align': 'right',
        })
        worksheet.set_column('A:A', 10)
        worksheet.set_column('B:B', 40)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 12)
        worksheet.set_column('F:F', 12)
        worksheet.merge_range(
            'A1:F1',
            'CW Salary Report From %s To %s' % (
                self.start_date,
                self.end_date,
            ),
            title_format,
        )
        row = 1
        employees = self.env['hr.employee'].search(
            [('active', '=', True)],
            order='id',
        )
        employee_number = 1
        for employee in employees:
            timesheets = self.env['account.analytic.line'].search([
                ('employee_id', '=', employee.id),
                ('date', '>=', self.start_date),
                ('date', '<=', self.end_date),
            ], order='date, id')

            start_datetime = fields.Datetime.to_datetime(
                self.start_date
            )

            end_datetime = fields.Datetime.to_datetime(
                self.end_date
            ).replace(
                hour=23,
                minute=59,
                second=59,
            )

            leaves = self.env['hr.leave'].search([
                ('employee_id', '=', employee.id),
                ('state', '=', 'validate'),
                ('date_from', '<=', end_datetime),
                ('date_to', '>=', start_datetime),
            ], order='date_from')
            if not timesheets and not leaves:
                continue
            worksheet.write(row, 0, 'ID', header_format)
            worksheet.write(row, 1, 'Employee', header_format)
            worksheet.write(row, 2, 'Start Date', header_format)
            worksheet.write(row, 3, 'End Date', header_format)
            worksheet.write(row, 4, 'Hours', header_format)
            worksheet.write(row, 5, 'Days', header_format)

            row += 1
            total_hours = sum(
                line.unit_amount or 0.0
                for line in timesheets
            )
            worksheet.write(
                row,
                0,
                employee_number,
                employee_format,
            )

            worksheet.write(
                row,
                1,
                employee.name,
                employee_format,
            )

            worksheet.write(
                row,
                2,
                '',
                employee_format,
            )

            worksheet.write(
                row,
                3,
                '',
                employee_format,
            )

            worksheet.write_number(
                row,
                4,
                total_hours,
                employee_hours_format,
            )

            worksheet.write(
                row,
                5,
                '',
                employee_format,
            )

            row += 1
            activity_hours = {}
            for line in timesheets:
                if line.project_id:
                    activity_name = line.project_id.name
                elif line.task_id:
                    activity_name = line.task_id.name
                else:
                    activity_name = line.name or 'Internal'
                if activity_name not in activity_hours:
                    activity_hours[activity_name] = 0.0
                activity_hours[activity_name] += (
                    line.unit_amount or 0.0
                )
            for activity_name, hours in activity_hours.items():
                worksheet.write(
                    row,
                    0,
                    '',
                    activity_format,
                )

                worksheet.write(
                    row,
                    1,
                    activity_name,
                    activity_format,
                )

                worksheet.write(
                    row,
                    2,
                    '',
                    activity_format,
                )

                worksheet.write(
                    row,
                    3,
                    '',
                    activity_format,
                )

                worksheet.write_number(
                    row,
                    4,
                    hours,
                    activity_hours_format,
                )

                worksheet.write(
                    row,
                    5,
                    '',
                    activity_format,
                )
                row += 1
            for leave in leaves:
                leave_type = (
                    leave.holiday_status_id.name
                    if leave.holiday_status_id
                    else 'Time Off'
                )

                leave_days = leave.number_of_days or 0.0

                worksheet.write(
                    row,
                    0,
                    '',
                    timeoff_format,
                )

                worksheet.write(
                    row,
                    1,
                    leave_type,
                    timeoff_format,
                )
                worksheet.write_datetime(
                    row,
                    2,
                    leave.date_from,
                    timeoff_date_format,
                )

                worksheet.write_datetime(
                    row,
                    3,
                    leave.date_to,
                    timeoff_date_format,
                )

                worksheet.write(
                    row,
                    4,
                    '',
                    timeoff_format,
                )

                worksheet.write_number(
                    row,
                    5,
                    leave_days,
                    timeoff_days_format,
                )

                row += 1
            row += 1
            employee_number += 1
        worksheet.freeze_panes(2, 0)
        worksheet.set_default_row(20)
        workbook.close()
        output.seek(0)
        file_data = base64.b64encode(
            output.read()
        )

        attachment = self.env['ir.attachment'].create({
            'name': 'CW_Salary_Report_%s_%s.xlsx' % (
                self.start_date,
                self.end_date,
            ),
            'type': 'binary',
            'datas': file_data,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': (
                'application/vnd.openxmlformats-officedocument.'
                'spreadsheetml.sheet'
            ),
        })
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }