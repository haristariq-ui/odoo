from odoo import api, fields, models

class product_pricelist(models.Model):
    _inherit = "product.pricelist.item"
    exchange_rate = fields.Float(string="Exchange Rate", digits=(16,4))

    def _compute_base_price(self, product, quantity, uom, date, currency, **kwargs ):
        currency.ensure_one()
        rule_base = self.base or 'list_price'
        if rule_base == 'pricelist' and self.base_pricelist_id:
            price = self.base_pricelist_id._get_product_price(
                product, quantity, currency=self.base_pricelist_id.currency_id, uom=uom, date=date,
                **kwargs
            )
            src_currency = self.base_pricelist_id.currency_id
        elif rule_base == "standard_price":
            src_currency = product.cost_currency_id
            price = product._price_compute(rule_base, uom=uom, date=date)[product.id]
        else:
            src_currency = product.currency_id
            price = product._price_compute(rule_base, uom=uom, date=date)[product.id]
        print("PRICE:", price)
        print("SOURCE CURRENCY:", src_currency.name)
        print("TARGET CURRENCY:", currency.name)
        print("COMPANY:", self.env.company.name)
        print("COMPANY ID:", self.env.company.id)
        print("COMPANY CURRENCY:", self.env.company.currency_id.name)
        print("COMPUTE PRICE:", self.compute_price)
        print("EXCHANGE RATE:", self.exchange_rate)

        if src_currency != currency:
            if self.compute_price == "formula" and self.exchange_rate:
                exchange_rate = self.exchange_rate
                company_currency = self.env.company.currency_id
                if src_currency == company_currency and currency != company_currency:
                    price = price * exchange_rate
                elif src_currency != company_currency and currency == company_currency:
                    price = price / exchange_rate
        return price