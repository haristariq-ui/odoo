from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    vendor_reference_no = fields.Char(string="Vendor Ref No")

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    slab_weight = fields.Float(string="Slab Weight")