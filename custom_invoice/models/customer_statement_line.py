from odoo import api, fields, models

class CustomerStatementLine(models.Model):
    _name = "customer.statement.line"
    _description = "Customer Statement Line"
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        required=True,
    )
    invoice_id = fields.Many2one(
        "account.move",
        string="Invoice",
    )
    number = fields.Char(string="Invoice Number")
    invoice_date = fields.Date(string="Invoice Date")
    invoice_total = fields.Monetary(string="Invoice Total",currency_field="currency_id")
    previous_balance = fields.Monetary(string="Previous Balance",currency_field="currency_id")
    total_payments = fields.Monetary(string="Payments",currency_field="currency_id")
    current_balance = fields.Monetary(string="Current Balance",currency_field="currency_id")
    currency_id = fields.Many2one(
        "res.currency",related="partner_id.currency_id",store=True,
    )