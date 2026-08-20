from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = "account.move"
    previous_balance = fields.Monetary(
        string="Previous Balance",
        compute="_compute_previous_balance",
        currency_field="currency_id",
        store=True,
    )
    current_balance = fields.Monetary(
        string="Current Balance",
        compute= "_compute_current_balance",
        currency_field="currency_id",
        store=True,
    )
    @api.depends("partner_id","amount_total","amount_residual")
    def _compute_previous_balance(self):
        for move in self:
            move.previous_balance=0.0

            previous_invoices=self.env["account.move"].search([
                ('partner_id','=',move.partner_id.id),
                ('move_type','=','out_invoice'),
                ('state','=','posted'),
                ('amount_residual', '>', 0),
                ('id', '!=', move.id),
                ]
            )
            move.previous_balance=sum(previous_invoices.mapped('amount_residual'))
    @api.depends("previous_balance", "amount_residual")
    def _compute_current_balance(self):
        for move in self:

            if move.state == 'posted':
                move.current_balance= move.previous_balance + move.amount_residual
            else:
                move.current_balance = move.previous_balance
