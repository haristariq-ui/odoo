from odoo import api, fields, models
class category(models.Model):
   _inherit = 'sale.order.line'
   category_id = fields.Many2one(
       "product.category",
       string="Category"
   )
   @api.onchange("product_id")
   def _onchange_product_id_category(self):
        if self.product_id:
            self.category_id = self.product_id.categ_id
        else:
            self.category_id = False
















