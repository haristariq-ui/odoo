from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        result = super().action_confirm()
        for order in self:
            if not order.partner_id:
                continue
            history = self.env['contact.history'].search(
                [
                    ('partner_id', '=', order.partner_id.id)
                ],limit=1)
            if not history:
                history = self.env['contact.history'].create({
                    'partner_id': order.partner_id.id,
                })
            for line in order.order_line:
                self.env['contact.history.line'].create({
                    'history_id': history.id,
                    'sale_order_id': order.id,
                    'product_id': line.product_id.id,
                    'description': line.name,
                    'unit_price': line.price_unit,
                    'product_quantity': line.product_uom_qty,
                })
        return result