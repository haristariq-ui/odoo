from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    priority = fields.Selection(
        [
            ('1', 'Highest'),
            ('2', 'Medium'),
            ('3', 'Lowest'),
        ],
        string='Stock Priority',
        default='2',
        required=True,
    )

    def _get_stock_priority(self):
        self.ensure_one()
        return {
            '1': '3',
            '2': '2',
            '3': '1',
        }.get(self.priority, '2')

    def _update_stock_picking_priority(self):
        for order in self:
            if order.state != 'sale':
                continue
            pickings = order.picking_ids.filtered(
                lambda picking: picking.state not in ('done', 'cancel')
            )
            if pickings:
                pickings.write({
                    'priority': order._get_stock_priority(),
                })

    def write(self, vals):
        result = super().write(vals)
        if 'priority' in vals:
            self._update_stock_picking_priority()
        return result