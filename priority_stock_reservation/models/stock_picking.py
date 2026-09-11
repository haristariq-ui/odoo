from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    priority = fields.Selection(
        [
            ('0', 'Normal'),
            ('1', 'Lowest'),
            ('2', 'Medium'),
            ('3', 'Highest'),
        ],
        string='Priority',
        default='0',
    )