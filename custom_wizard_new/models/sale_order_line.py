from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    custom_vendor_id = fields.Many2one(
        "res.partner",
        string="Purchase Vendor",
    )

    purchase_line_ids = fields.One2many(
        "purchase.order.line",
        "sale_line_id",
        string="Purchase Lines",
    )

    purchase_order_id = fields.Many2one(
        "purchase.order",
        string="Purchase Order",
        compute="_compute_purchase_order_id",
    )

    @api.depends("purchase_line_ids.order_id")
    def _compute_purchase_order_id(self):
        for line in self:
            line.purchase_order_id = line.purchase_line_ids[:1].order_id

    def action_open_vendor_wizard(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Vendor Data",
            "res_model": "vendor.data.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_product_id": self.product_id.id,
                "default_sale_order_line_id": self.id,
            },
        }