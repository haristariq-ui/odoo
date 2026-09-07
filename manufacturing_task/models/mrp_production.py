from odoo import fields, models

class MrpProduction(models.Model):
    _inherit = "mrp.production"

    sale_order_id = fields.Many2one(
        "sale.order",
        string="Sale Order"
    )
    customer_name = fields.Char(
        string="Customer Name"
    )
    invoice_address = fields.Text(
        string="Invoice Address"
    )
    delivery_address = fields.Text(
        string="Delivery Address"
    )
    unit_number = fields.Char(
        string="Unit Number"
    )
    component_status = fields.Selection(
        [
            ("available", "Available"),
            ("unavailable", "Unavailable"),
        ],
        string="Component Status"
    )
    barcode_labels_qty = fields.Integer(
        string="Barcode Labels Qty",
        default=1
    )
    effective_date = fields.Date(
        string="Effective Date"
    )
    tentative_temp_date = fields.Date(
        string="Tentative Temp Date"
    )
    airtable = fields.Char(
        string="Airtable"
    )
    remarks = fields.Text(
        string="Remarks"
    )
    start_date = fields.Date(
        string="Start Date"
    )
    end_date = fields.Date(
        string="End Date"
    )
    script_done = fields.Boolean(
        string="Script Done"
    )
    done_mo = fields.Boolean(
        string="Done MO"
    )
    def action_print_bom_label(self):
        self.ensure_one()
        return self.env.ref(
            "manufacturing_task.action_report_bom_label"
        ).report_action(self)