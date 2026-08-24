from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    customer_category = fields.Selection(
        related="partner_id.customer_category",
        string="Customer Category",
        store=True,
        readonly=False,
    )