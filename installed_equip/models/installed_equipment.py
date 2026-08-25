from odoo import models, fields,api

class InstalledEquipment(models.Model):
    _name = "installed.equipment"
    _description = "Installed Equipment"

    product_id = fields.Many2one(
        "product.product",
        string="Product",

    )
    lot_id = fields.Many2one(
        "stock.lot",
        string="Lot/Serial Number",

    )
    sale_order_id = fields.Many2one(
        "sale.order",
        string="Sale Order",

    )
    delivery_order_id = fields.Many2one(
        "stock.picking",
        string="Delivery Order",

    )
    customer_id = fields.Many2one(
        "res.partner",
        string="Customer",
    )
    stock_move_line_id = fields.Many2one(
        "stock.move.line",
        string="Stock Move Line",
    )
    installation_date = fields.Date(
        string="Installation Date",
    )
    delivery_date = fields.Date(
        string="Delivery Date",

    )
    installed_at_current_location = fields.Boolean(
        string="Installed at current location",

    )
    rec_d_into_inventory = fields.Boolean(
        string="Rec D Into Inventory",

    )
    @api.onchange("lot_id")
    def _onchange_lot_id(self):
        if self.lot_id:
            self.rec_d_into_inventory = self.lot_id.rec_d_into_inventory
        else:
            self.rec_d_into_inventory = False

