from odoo import models, fields

class StockLot(models.Model):
    _inherit = "stock.lot"

    rec_d_into_inventory = fields.Boolean(
        string="Rec D Into Inventory"
    )