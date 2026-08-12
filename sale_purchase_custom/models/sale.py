from odoo import api,models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"
    sales_channel = fields.Selection(
        [
            ('marketing', 'Marketing'),
            ('trade', 'Trade'),
            ('ecommerce', 'Ecommerce'),
        ],
        string='Sales Channel',
    )

    custom_order_type = fields.Char(string="Custom Order Type")

    total_discount = fields.Monetary(
        string="Total Discount",
        compute="_compute_display_discount",
        currency_field="currency_id",
        store=True,
    )

    @api.depends("order_line.discount_amount")
    def _compute_display_discount(self):
        for order in self:
            order.total_discount = sum(
                order.order_line.mapped("discount_amount")
            )
#     @api.depends('order_line')
#     def _compute_display_discount(self):
#         for rec in self:
#             rec.total_discount = sum(
#                 rec.order_line.mapped("discount_amount")
#             )
#             # rec.total_discount =0.00
#             # total = 0.00
#             # for line in rec.order_line:
#             #     total += line.discount_amount
#             # rec.total_discount = total
#
#     @api.depends(
#         "order_line.price_subtotal",
#         "currency_id",
#         "company_id",
#         "order_line.discount_amount",
#     )
#     def _compute_tax_totals(self):
#         super()._compute_tax_totals()
#
#         for order in self:
#             if not order.tax_totals:
#                 continue
#
#             tax_totals = dict(order.tax_totals)
#
#             subtotal = {
#                 "name": "Discount like untaxed amount font",
#                 "base_amount_currency": order.total_discount,
#                 "tax_groups": [],
#             }
#             tax_totals["subtotals"].insert(1, subtotal)
#
#             order.tax_totals = tax_totals
# #-------------------------------------------------------------------------------
#             subtotal = tax_totals["subtotals"][0]
#             discount = {
#                 "group_name": "discount like tax 15%",
#                 "tax_amount_currency": order.total_discount,
#
#             }
#             subtotal["tax_groups"].insert(1, discount)
#             order.tax_totals= tax_totals
class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.model
    def _get_tax_totals_summary(
        self,
        base_lines,
        currency,
        company,
        **kwargs
    ):
        tax_totals_summary = super()._get_tax_totals_summary(
            base_lines=base_lines,
            currency=currency,
            company=company,
            **kwargs
        )

        total_discount = sum(
            line.get("discount_amount", 0.0)
            for line in base_lines
        )

        if total_discount and tax_totals_summary.get("subtotals"):
            subtotal = tax_totals_summary["subtotals"][0]

            discount_subtotal = {
                "group_name": "Discount by haris",
                "tax_amount_currency": total_discount,

            }
            subtotal["tax_groups"].insert( 1,discount_subtotal)
        return tax_totals_summary

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    custom_size = fields.Char(string="Size")

    discount_amount = fields.Monetary(
        string="Discount",
        currency_field="currency_id",
    )

    tax_amount = fields.Monetary(
        string="Tax amount",
        compute="_compute_discount_tax_amount",
        currency_field="currency_id",
        store=True,
    )

    def _prepare_base_line_for_taxes_computation(self, **kwargs):
        base_line = super()._prepare_base_line_for_taxes_computation(
            **kwargs
        )

        base_line["discount_amount"] = self.discount_amount

        return base_line


    @api.onchange("discount_amount", "price_unit", "product_uom_qty")
    def _onchange_discount_amount(self):
        for line in self:
            total = line.price_unit * line.product_uom_qty
            if total:
                line.discount = (line.discount_amount / total) * 100
            else:
                line.discount = 0.0

    @api.depends(
        "price_unit",
        "product_uom_qty",
        "discount",
        "tax_ids"
    )
    def _compute_discount_tax_amount(self):
        for line in self:
            discounted_price = line.price_unit * (
                    1 - line.discount / 100
            )
            taxes = line.tax_ids.compute_all(
                discounted_price,
                currency=line.currency_id,
                quantity=line.product_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_shipping_id,
            )

            line.tax_amount = taxes["total_included"] - taxes["total_excluded"]

