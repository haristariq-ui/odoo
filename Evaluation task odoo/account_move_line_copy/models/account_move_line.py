from odoo import models, _
from odoo.exceptions import UserError

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def action_copy_move_line(self):
        self.ensure_one()
        move = self.move_id
        if not move:
            raise UserError(_("This line is not linked to an accounting move"))
        if self.display_type != 'product':
            raise UserError(_("Only product invoice lines can be copied"))
        if move.state != 'draft':
            raise UserError(
                _("You can only copy invoice lines while the invoice is in Draft")
            )
        vals = {
            'move_id': move.id,
            'product_id': self.product_id.id,
            'name': self.name,
            'quantity': self.quantity,
            'product_uom_id': self.product_uom_id.id,
            'price_unit': self.price_unit,
            'discount': self.discount,
            'tax_ids': [(6, 0, self.tax_ids.ids)],
            'account_id': self.account_id.id,
            'analytic_distribution': self.analytic_distribution,
        }
        new_line = self.env['account.move.line'].create(vals)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }