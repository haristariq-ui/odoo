from odoo import models, fields
from odoo.exceptions import UserError


class LibraryBook(models.Model):
    _name = "library.book"

    name = fields.Char(required=True)
    author = fields.Char()
    price = fields.Float()
    cost_price = fields.Float(
        string="Cost Price",
        groups="library_management.group_library_manager"
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("approved", "Approved"),
        ],
        default="draft"
    )
    def action_approve(self):

        if not self.env.user.has_group(
                "library_management.group_library_manager"
        ):
            raise UserError(
                "Only Library Managers can approve books."
            )
        self.state = "approved"
