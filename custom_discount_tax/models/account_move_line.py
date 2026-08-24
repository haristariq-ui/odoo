from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    discount_amount = fields.Monetary(
        string="Discount Amount",
        currency_field="currency_id",
        compute="_compute_discount_tax_amount",
        store=True,
    )
    tax_amount = fields.Monetary(
        string="Tax Amount",
        currency_field="currency_id",
        compute="_compute_discount_tax_amount",
        store=True,
    )
    @api.depends(
        "price_unit","quantity","discount","tax_ids",
    )
    def _compute_discount_tax_amount(self):
        for line in self:
            gross_amount = line.quantity * line.price_unit
            discount_amount=(
                gross_amount * line.discount/100
            )
            line.discount_amount = discount_amount
            taxable_amount = gross_amount - discount_amount
            tax_amount = 0.0
            if line.tax_ids:
                tax = line.tax_ids[0]
                tax_amount = taxable_amount * tax.amount / 100

            line.tax_amount = tax_amount
