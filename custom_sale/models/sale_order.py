from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    confirm_ = fields.Boolean( string='Confirmed', default=False)

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            order.confirm_ = True
        return res

    def action_cancel(self):
        res = super().action_cancel()
        for order in self:
            order.confirm_ = False
        return res