from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        vals = super()._prepare_invoice_line(**optional_values)
        vals.update({
            "discount_amount": self.discount_amount,
            "tax_amount": self.tax_amount,
        })
        return vals