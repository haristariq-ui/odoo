import base64
import io
import xlsxwriter
from odoo import models

class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def action_print_pricelist_pdf(self):
        self.ensure_one()
        return self.env.ref(
            "custom_pricelist_report.action_report_pricelist_pdf"
        ).report_action(self)
    def action_export_pricelist_excel(self):
        self.ensure_one()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {
            "in_memory": True,
        })
        worksheet = workbook.add_worksheet("Pricelist")
        title_format = workbook.add_format({
            "bold": True,
            "font_size": 14,
        })
        header_format = workbook.add_format({
            "bold": True,
            "border": 1,
        })
        cell_format = workbook.add_format({
            "border": 1,
        })
        price_format = workbook.add_format({
            "border": 1,
            "num_format": "0.00",
        })
        worksheet.set_column("A:A", 20)
        worksheet.set_column("B:B", 35)
        worksheet.set_column("C:C", 20)
        worksheet.write("A1", self.name, title_format)
        worksheet.write("A2","Currency",header_format,)
        worksheet.write("B2",self.currency_id.name or "", cell_format,)
        row = 4
        worksheet.write(row, 0, "Product Code", header_format)
        worksheet.write(row, 1, "Product Description", header_format)
        worksheet.write( row, 2, "Unit Price (%s)" % self.currency_id.name, header_format, )
        row += 1
        for line in self.item_ids:
            if not line.product_tmpl_id:
                continue
            product = line.product_tmpl_id
            worksheet.write( row,  0,product.product_variant_id.default_code or "", cell_format, )
            worksheet.write(row,1,product.name or "",cell_format,)
            worksheet.write_number(row,2,line.fixed_price,price_format,)
            row += 1
        workbook.close()
        output.seek(0)
        file_data = output.read()
        output.close()
        attachment = self.env["ir.attachment"].create({
            "name": "%s.xlsx" % self.name,
            "type": "binary",
            "datas": base64.b64encode(file_data),
            "res_model": self._name,
            "res_id": self.id,
            "mimetype": (
                "application/"
                "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
        })
        return {
            "type": "ir.actions.act_url",
            "url": "/web/content/%s?download=true" % attachment.id,
            "target": "self",
        }