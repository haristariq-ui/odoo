from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    customer_category = fields.Selection(
        related="partner_id.customer_category",
        string="Customer Category",
        store=True,
        readonly=False,
    )