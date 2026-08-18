from odoo import api, fields, models
class CustomWizard(models.TransientModel):
    _name = 'vendor.data.wizard'
    _description = 'vendor data wizard'
    product_id = fields.Many2one('product.product',string='Product',readonly=True)
    default_code = fields.Char(
        string="Internal Reference",
        related="product_id.default_code",
        readonly=True
    )
    categ_id = fields.Many2one(
        "product.category",
        string="Category",
        related="product_id.categ_id",
        readonly=True
    )
    list_price = fields.Float(
        string="Sales Price",
        related="product_id.list_price",
        readonly=True
    )
    vendor_line_ids = fields.One2many(
        "vendor.data.wizard.line",
        "wizard_id",
        string="Vendor Lines"
    )

    def action_get_data(self):
        self.vendor_line_ids.unlink()

        for seller in self.product_id.seller_ids:
            self.env["vendor.data.wizard.line"].create({
                "wizard_id": self.id,
                "vendor_id": seller.partner_id.id,
                "price": seller.price,
                "min_qty": seller.min_qty,
                "delay": seller.delay,
            })

        return {
            "type": "ir.actions.act_window",
            "res_model": "vendor.data.wizard",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }
class VendorDataWizardLine(models.TransientModel):
        _name = "vendor.data.wizard.line"
        _description = "Vendor Data Wizard Line"
        wizard_id = fields.Many2one(
            "vendor.data.wizard",
            string="Wizard",
            required=True,
            ondelete="cascade"
        )
        vendor_id = fields.Many2one(
            "res.partner",
            string="Vendor",
            readonly=True
        )
        price = fields.Float(
            string="Vendor Price",
            readonly=True
        )
        min_qty = fields.Float(
            string="Min Quantity",
            readonly=True
        )
        delay = fields.Integer(
            string="Delivery Time",
            readonly=True
        )