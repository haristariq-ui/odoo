from odoo import api,fields,models

class ResPartner(models.Model):
    _inherit = "res.partner"
    statement_line_ids = fields.One2many(
        "customer.statement.line",
        "partner_id",
        string="Customer Statement",
        compute="_compute_customer_statement",
    )
    total_amount_due = fields.Monetary(
        string="Total Amount Due",
        currency_field="currency_id",
        compute="_compute_customer_statement",
    )
    def _compute_customer_statement(self):
        print("haris")
        StatementLine = self.env["customer.statement.line"]
        for partner in self:
            invoices = self.env["account.move"].search([
                ("partner_id", "=", partner.id),
                ("move_type", "=", "out_invoice"),
                ("state", "=", "posted"),
            ], order="invoice_date desc")
            previous_balance = 0.0
            total_due = 0.0
            for invoice in invoices:
                total_payments = (
                       invoice.amount_total - invoice.amount_residual )
                current_balance = (previous_balance + invoice.amount_residual)
                line = StatementLine.create({
                    "partner_id": partner.id,
                    "invoice_id": invoice.id,
                    "number": invoice.name,
                    "invoice_date": invoice.invoice_date,
                    "invoice_total": invoice.amount_total,
                    "previous_balance": previous_balance,
                    "total_payments": total_payments,
                    "current_balance": current_balance,
                })
                StatementLine += line
                previous_balance = current_balance
                total_due += invoice.amount_residual
            partner.statement_line_ids = StatementLine
            # partner.statement_line_ids = [(6,0,StatementLine.ids)]
            partner.total_amount_due = total_due