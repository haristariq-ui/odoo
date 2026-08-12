from odoo import models, fields

class StockPicking(models.Model):
    _inherit = "stock.picking"

    transporter_name = fields.Char(string="Transporter")

class StockMove(models.Model):
    _inherit = "stock.move"

    pallet_no = fields.Char(string="Pallet No")