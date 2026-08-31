from odoo import fields, models

class StockQuant(models.Model):
    _inherit = "stock.quant"
    can_edit_inventoried_qty = fields.Boolean(
        compute="_compute_can_edit_inventoried_qty"
    )
    def _compute_can_edit_inventoried_qty(self):
        can_edit = self.env.user.has_group(
            "custom_permission.group_edit_inventoried_qty"
        )
        for quant in self:
            quant.can_edit_inventoried_qty = can_edit