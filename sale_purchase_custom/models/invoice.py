from odoo import api,models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    custom_invoice_type = fields.Char(string="Custom Invoice Type")
    tog_button = fields.Boolean(string='Address', default=False)

    custom_street = fields.Char(compute="_compute_address",inverse="_inverse_address", store=True)
    custom_street2 = fields.Char(compute="_compute_address",inverse="_inverse_address", store=True)
    custom_city = fields.Char(compute="_compute_address",inverse="_inverse_address", store=True)
    custom_zip = fields.Char(compute="_compute_address",inverse="_inverse_address", store=True)
    custom_state_id = fields.Many2one(
        "res.country.state",
        string="Customer State",
        compute="_compute_address",
        inverse = "_inverse_address",
        store=True,
    )
    custom_country_id = fields.Many2one(
        "res.country",
        string="Customer Country",
        compute="_compute_address",
        inverse = "_inverse_address",
        store=True
    )

    @api.depends(
        "tog_button",
        "partner_id",
        "partner_id.zip",
    )
    def _compute_address(self):
      for rec in self:
        if rec.tog_button and rec.partner_id:
            partner = rec.partner_id
            rec.custom_street = partner.street
            rec.custom_street2 = partner.street2
            rec.custom_city = partner.city
            rec.custom_zip = partner.zip
            rec.custom_state_id = partner.state_id
            rec.custom_country_id = partner.country_id
        else:
            rec.custom_street = False
            rec.custom_street2 = False
            rec.custom_city = False
            rec.custom_zip = False
            rec.custom_state_id = False
            rec.custom_country_id = False

    @api.onchange("tog_button")
    def _onchange_toggle(self):
        self.custom_invoice_type = "Toggle Changed"

    def _inverse_address(self):
        for rec in self:
            partner = rec.partner_id
            if partner:
                if rec.custom_state_id:
                    state = rec.custom_state_id.id
                else:
                    state= False
                if rec.custom_country_id:
                    country = rec.custom_country_id.id
                else:
                    country = False
                partner.write({
                    "street": rec.custom_street,
                    "street2": rec.custom_street2,
                    "city": rec.custom_city,
                    "zip": rec.custom_zip,
                    "state_id": state,
                    "country_id": country,
                })

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    custom_size = fields.Char(string="Size")