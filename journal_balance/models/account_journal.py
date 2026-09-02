from odoo import fields, models,api

class AccountJournal(models.Model):
    _inherit = "account.journal"

    balance = fields.Monetary(
        string="Balance",
        currency_field="currency_id",

    )
    def _fill_bank_cash_dashboard_data(self, dashboard_data):
        super()._fill_bank_cash_dashboard_data(dashboard_data)
        bank_cash_journals = self.filtered(
            lambda journal: journal.type in ("bank", "cash", "credit")
        )
        outstanding_payments = bank_cash_journals._get_journal_dashboard_outstanding_payments()
        for journal in bank_cash_journals:
            outstanding_balance = outstanding_payments.get(
                journal.id, (0, 0)
            )[1]
            balance = journal.current_statement_balance + outstanding_balance
            journal.write({
                "balance": balance,
            })