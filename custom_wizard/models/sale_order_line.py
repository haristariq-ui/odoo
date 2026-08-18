from odoo import api,fields,models
class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    def action_confirm(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'vendor data',
            'res_model': 'vendor.data.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_product_id': self.product_id.id
            }
        }