from odoo import models, fields, api
import io
import json

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class DynamicContactReport(models.Model):
    _name = "dynamic.contact.report"

    contact_report = fields.Char(string="Contact Report")
    date_from = fields.Datetime(string="Date From")
    date_to = fields.Datetime(string="Date to")
    report_type = fields.Selection([
        ('report_by_contact', 'Report By Contact'),
        ('report_by_activity', 'Report By Activity'),
        ('report_by_tags', 'Report By Tags'),
        ('report_by_country', 'Report By Country'),
        ('report_by_sales_representative', 'Report By Sales Representative'),
        ('report_by_state', 'Report By State')], default='report_by_contact')

    @api.model
    def contact_report(self, option):
        report_values = self.env['dynamic.contact.report'].search(
            [('id', '=', option[0])])
        data = {
            'report_type': report_values.report_type,
            'model': self,
        }
        if report_values.date_from:
            data.update({
                'date_from': report_values.date_from,
            })
        if report_values.date_to:
            data.update({
                'date_to': report_values.date_to,
            })
        filters = self.get_filter(option)
        lines = self._get_report_values(data).get('CONTACT')
        sub_line = self.get_report_child_lines()
        return {
            'name': "Contacts Report",
            'type': 'ir.actions.client',
            'tag': 'c_r',  # Tag para contactos
            'contacts': data,
            'filters': filters,
            'report_lines': lines,
        }

    def _get_report_sub_lines(self, data, report, date_from, date_to):
        report_sub_lines = []
        if data.get('report_type') == 'report_by_contact':
            query = '''
                SELECT p.name, p.create_date, p.country_id, p.email, p.phone, p.user_id, 
                       p.category_id, u.partner_id as user_partner,
                       c.name as country_name, rp.name as representative_name
                FROM res_partner as p
                LEFT JOIN res_users as u ON p.user_id = u.id
                LEFT JOIN res_country as c ON p.country_id = c.id
                LEFT JOIN res_partner as rp ON u.partner_id = rp.id
                WHERE p.is_company = false  -- Ajusta según tus necesidades
            '''
            term = 'AND '
            if data.get('date_from'):
                query += "AND p.create_date >= '%s' " % data.get('date_from')
            if data.get('date_to'):
                query += term + "p.create_date <= '%s' " % data.get('date_to')
            query += "GROUP BY p.name, p.create_date, p.country_id, p.email, p.phone, p.user_id, " \
                     "p.category_id, u.partner_id, c.name, rp.name"
            self._cr.execute(query)
            report_by_contact = self._cr.dictfetchall()
            report_sub_lines.append(report_by_contact)
        return report_sub_lines

    def get_filter(self, option):
        # Implementar el método de filtros según tus necesidades para contactos
        pass

    def _get_report_values(self, data):
        # Implementar lógica para obtener valores del reporte según los datos y tipo de reporte
        return {}

    def get_report_child_lines(self):
        # Implementar lógica para obtener líneas hijas del reporte
        return {}