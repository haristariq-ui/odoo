from odoo import models
class StockRule(models.Model):
    _inherit = "stock.rule"
    def _get_matching_supplier(
        self,
        product,
        quantity,
        uom,
        company,
        values,
    ):
        supplierinfo = values.get("supplierinfo_id")
        if supplierinfo:
            return supplierinfo
        sale_line_id = values.get("sale_line_id")
        if sale_line_id:
            sale_line = self.env["sale.order.line"].browse(sale_line_id)
            if sale_line.exists() and sale_line.custom_vendor_id:
                supplierinfo = product._select_seller(
                    partner_id=sale_line.custom_vendor_id,
                    quantity=quantity,
                    uom_id=uom,
                )
                if supplierinfo:
                    return supplierinfo
        return super()._get_matching_supplier(
            product,
            quantity,
            uom,
            company,
            values,
        )