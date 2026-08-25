from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    installed_equipment_ids = fields.One2many(
        "installed.equipment",
        "delivery_order_id",
        string="Installed Equipments",
        compute="_compute_installed_equipment",
        store=True,
    )
    @api.depends(
        "move_line_ids",
        "move_line_ids.lot_id",
    )
    def _compute_installed_equipment(self):
        self.installed_equipment_ids.unlink()
        InstalledEquipment = self.env["installed.equipment"]
        for picking in self:
            for move_line in picking.move_line_ids:
                if not move_line.product_id.is_equipment:
                    continue
                # sale_order = move_line.move_id.sale_line_id.order_id
                sale_order = picking.sale_id
                if picking.sale_id:
                    sale_order= picking.sale_id
                else:
                    sale_order = False
                InstalledEquipment.create({
                    "delivery_order_id": picking.id,
                    "stock_move_line_id": move_line.id,
                    "product_id": move_line.product_id.id,
                    "lot_id": move_line.lot_id.id,
                    "sale_order_id": sale_order.id if sale_order else False,
                    "customer_id": picking.partner_id.id,
                    "delivery_date": (
                        picking.scheduled_date.date()
                        if picking.scheduled_date
                        else False
                    ),
                    "rec_d_into_inventory": (
                        move_line.lot_id.rec_d_into_inventory
                        if move_line.lot_id
                        else False
                    ),
                })
