from odoo import fields, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    type_tax_use = fields.Selection(
        selection_add=[
            ('use', 'Use'),
        ],
        ondelete={
            'use': 'set default',
        },
    )