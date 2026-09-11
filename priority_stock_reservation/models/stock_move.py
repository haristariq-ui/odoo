from odoo import fields, models

class StockMove(models.Model):
    _inherit = 'stock.move'
    priority = fields.Selection(
        [
            ('0', 'Normal'),
            ('1', 'Lowest'),
            ('2', 'Medium'),
            ('3', 'Highest'),
        ],
        string='Priority',
        compute='_compute_priority',
        store=True,
    )
    def _compute_priority(self):
        for move in self:
            move.priority = move.picking_id.priority or '0'

    def _get_sale_order(self):
        self.ensure_one()
        if self.sale_line_id:
            return self.sale_line_id.order_id
        if self.group_id.sale_id:
            return self.group_id.sale_id
        return self.env['sale.order']

    def _get_new_picking_values(self):
        vals = super()._get_new_picking_values()
        sale_order = self._get_sale_order()
        if sale_order:
            vals['priority'] = sale_order._get_stock_priority()
        return vals

    def _key_assign_picking(self):
        key = super()._key_assign_picking()
        sale_order = self._get_sale_order()
        if sale_order:
            return key + (sale_order.priority,)
        return key + (False,)