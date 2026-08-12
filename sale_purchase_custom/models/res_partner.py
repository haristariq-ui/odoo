from odoo import api, fields, models
class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_view_customer_invoices(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoices',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [
                ('partner_id', '=', self.id),
                ('move_type', '=', 'out_invoice'),
            ],
            'context': {
                'default_partner_id': self.id,
                'default_move_type': 'out_invoice',
            },
        }