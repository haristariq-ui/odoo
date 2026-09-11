from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_ids = fields.Many2many(
        'res.partner',
        string='Partner IDs',
    )

    def action_send_to_partners(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Send Sale Order',
            'res_model': 'sale.partner.email.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref(
                'custom_sale_partner_email.sale_partner_email_wizard_form'
            ).id,
            'target': 'new',
            'context': {
                'default_sale_order_id': self.id,
                'default_partner_ids': [(6, 0, self.partner_ids.ids)],
            },
        }