from odoo import fields, models
from odoo.exceptions import UserError


class SalePartnerEmailWizard(models.TransientModel):
    _name = 'sale.partner.email.wizard'

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        readonly=True,
    )
    partner_ids = fields.Many2many(
        'res.partner',
        string='Recipients',
        required=True,
    )
    def action_send(self):
        self.ensure_one()
        if not self.partner_ids:
            raise UserError('Please select at least one partner.')
        partners_without_email = self.partner_ids.filtered(
            lambda partner: not partner.email
        )
        if partners_without_email:
            names = ', '.join(partners_without_email.mapped('name'))
            raise UserError(
                f'The following partners do not have an email address:\n{names}'
            )
        template = self.env.ref(
            'custom_sale_partner_email.email_template_custom_sale_order_confirmation'
        )
        compose_form = self.env.ref(
            'mail.email_compose_message_wizard_form'
        )
        return {
            'name': 'Compose Email',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': compose_form.id,
            'res_model': 'mail.compose.message',
            'target': 'new',
            'context': {
                'default_model': 'sale.order',
                'default_res_ids': [self.sale_order_id.id],
                'default_template_id': template.id,
                'default_composition_mode': 'comment',
                'default_partner_ids': self.partner_ids.ids,
                'force_email': True,
            },
        }