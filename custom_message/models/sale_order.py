from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    custom_message = fields.Text(
        string='Custom Message'
    )