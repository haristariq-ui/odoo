from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    customer_category = fields.Selection(
        [
            ("retail", "Retail"),
            ("wholesale", "Wholesale"),
            ("corporate", "Corporate"),
        ],
        string="Customer Category",
    )