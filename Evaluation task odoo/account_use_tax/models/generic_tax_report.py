from collections import defaultdict
from odoo import _, models


class GenericTaxReportCustomHandler(models.AbstractModel):
    _inherit = 'account.generic.tax.report.handler'

    def _dynamic_lines_generator(self, report, options, all_column_groups_expression_totals, warnings=None):
        dynamic_lines = list(super()._dynamic_lines_generator(report, options, all_column_groups_expression_totals, warnings=warnings))

        use_taxes = self.env['account.tax'].with_context(active_test=False).search([ ('type_tax_use', '=', 'use') ])
        if not use_taxes:
            return dynamic_lines
        company_ids = (
            report.get_report_company_ids(options)
            if hasattr(report, 'get_report_company_ids')
            else self.env.companies.ids
        )
        domain = [
            ('parent_state', '=', 'posted'),
            ('company_id', 'in', company_ids),
            '|',
            ('tax_ids', 'in', use_taxes.ids),
            ('tax_line_id', 'in', use_taxes.ids),
        ]

        date_from = options.get('date', {}).get('date_from')
        date_to = options.get('date', {}).get('date_to')
        if date_from:
            domain.append(('date', '>=', date_from))
        if date_to:
            domain.append(('date', '<=', date_to))
        move_lines = self.env['account.move.line'].search(domain)
        if not move_lines:
            return dynamic_lines
        tax_data = defaultdict(lambda: {'net': 0.0, 'tax': 0.0})
        for aml in move_lines:
            if aml.tax_line_id and aml.tax_line_id.type_tax_use == 'use':
                tax_data[aml.tax_line_id]['tax'] += aml.balance
            for applied_tax in aml.tax_ids:
                if applied_tax.type_tax_use == 'use':
                    tax_data[applied_tax]['net'] += aml.balance

        section_id = report._get_generic_line_id(None, None, markup='use_section')
        sub_lines = []
        total_tax_amount = 0.0

        for tax, vals in tax_data.items():
            net_val = vals['net']
            tax_val = vals['tax']
            total_tax_amount += tax_val

            tax_label = f"{tax.name} ({tax.amount}%)" if tax.amount else tax.name
            line_id = report._get_generic_line_id('account.tax', tax.id, parent_line_id=section_id)

            row_columns = []
            for col in options.get('columns', []):
                expr_label = col.get('expression_label')
                val = tax_val if expr_label == 'tax' else (net_val if expr_label == 'net' else 0.0)
                row_columns.append(report._build_column_dict(val, col, options=options))
            sub_line_dict = {
                'id': line_id,
                'name': tax_label,
                'level': 2,
                'parent_id': section_id,
                'columns': row_columns,
                'action': 'action_audit_cell',
                'action_params': {
                    'report_line_id': line_id,
                    'expression_label': 'tax',
                    'column_group_key': options['columns'][0]['column_group_key'] if options.get('columns') else None,
                },
            }
            sub_lines.append((0, sub_line_dict))
        header_columns = []
        for col in options.get('columns', []):
            val = total_tax_amount if col.get('expression_label') == 'tax' else None
            header_columns.append(report._build_column_dict(val, col, options=options))
        use_section_line = (0, {
            'id': section_id,
            'name': _('Use'),
            'level': 1,
            'unfoldable': False,
            'unfolded': True,
            'columns': header_columns,
        })
        dynamic_lines.append(use_section_line)
        dynamic_lines.extend(sub_lines)

        return dynamic_lines