from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_equipment = fields.Boolean(
        string="Is Equipment"
    )