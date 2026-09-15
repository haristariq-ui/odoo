from markupsafe import Markup, escape
from odoo import api, models

class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.depends(
        'model',
        'res_domain',
        'res_ids',
        'template_id',
    )
    def _compute_body(self):
        super()._compute_body()
        standard_template = self.env.ref(
            'sale.mail_template_sale_confirmation',
            raise_if_not_found=False,
        )
        for composer in self:
            if (
                not standard_template
                or composer.template_id != standard_template
            ):
                continue
            if composer.model != 'sale.order':
                continue
            res_ids = composer._evaluate_res_ids()
            if len(res_ids) != 1:
                continue
            sale_order = self.env['sale.order'].browse(res_ids[0])
            if not sale_order.exists():
                continue
            if not sale_order.custom_message:
                continue
            custom_message = escape(
                sale_order.custom_message
            ).replace('\n', Markup('<br/>'))

            custom_html = Markup("""
                <br/>
                <div>
                    <p>
                        <strong>Custom Message:</strong>
                    </p>
                    <p>
            """) + custom_message + Markup("""
                    </p>
                </div>
            """)
            composer.body = (composer.body or Markup('')) + custom_html