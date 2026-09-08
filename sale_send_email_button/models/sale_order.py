from odoo import _, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_custom_send_email(self):
        self.ensure_one()
        template = self.env.ref(
            "sale_send_email_button.email_template_custom_sale_order_confirmation"
        )
        compose_form = self.env.ref(
            "mail.email_compose_message_wizard_form"
        )
        ctx = {
            "default_model": "sale.order",
            "default_res_ids": self.ids,
            "default_use_template": True,
            "default_template_id": template.id,
            "default_composition_mode": "comment",
            "default_email_layout_xmlid": "mail.mail_notification_layout_with_responsible_signature",
            "force_email": True,
            "mark_so_as_sent": True,
        }
        return {
            "name": _("Compose Email"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form.id, "form")],
            "view_id": compose_form.id,
            "target": "new",
            "context": ctx,
        }
