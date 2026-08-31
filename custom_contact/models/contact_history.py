from odoo import models, fields

class ContactHistory(models.Model):
    _name = 'contact.history'
    _rec_name = 'partner_id'
    _order = 'id desc'
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner Name',
        required=True,
    )
    history_line_ids = fields.One2many(
        'contact.history.line',
        'history_id',
        string='History Lines'
    )
    invoice_ids = fields.Many2many(
        'account.move',
        'contact_history_invoice_rel',
        'history_id',
        'invoice_id',
        string='Invoices',
        domain=[
            ('move_type', 'in', ['out_invoice', 'out_refund'])
        ],
    )

    def action_sync_history(self):

        SaleOrder = self.env['sale.order']
        AccountMove = self.env['account.move']
        HistoryLine = self.env['contact.history.line']
        for history in self:
            partner = history.partner_id
            if not partner:
                continue
            history.history_line_ids.unlink()
            sale_orders = SaleOrder.search(
                [
                    ('partner_id', '=', partner.id),
                    ('state', '=', 'sale'),
                ],
                order='date_order desc, id desc',
            )
            for order in sale_orders:
                for line in order.order_line:
                    if not line.product_id:
                        continue

                    HistoryLine.create({
                        'history_id': history.id,
                        'sale_order_id': order.id,
                        'product_id': line.product_id.id,
                        'description': line.name,
                        'unit_price': line.price_unit,
                        'product_quantity': line.product_uom_qty,
                    })

            invoices = AccountMove.search(
                [
                    ('partner_id', '=', partner.id),
                    ('move_type', 'in', [
                        'out_invoice',
                        'out_refund',
                    ]),
                ],
                order='invoice_date desc, id desc',
            )
            history.invoice_ids = [(6, 0, invoices.ids)]
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
class ContactHistoryLine(models.Model):
    _name = 'contact.history.line'

    history_id = fields.Many2one(
        'contact.history',
        string='Contact History',
        required=True,
    )
    sale_order_id = fields.Many2one(
        'sale.order',
        string='Source Document'
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product Name'
    )
    description = fields.Char(
        string='Description'
    )
    unit_price = fields.Float(
        string='Unit Price'
    )
    product_quantity = fields.Float(
        string='Product Quantity'
    )