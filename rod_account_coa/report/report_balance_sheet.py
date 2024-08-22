from odoo import models, api
from odoo.exceptions import UserError


class ReportBalanceSheet(models.AbstractModel):
    _name = 'report.rod_account_coa.balance_sheet_pdf'
    _description = 'Balance Sheet PDF Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data:
            raise UserError('No data to print')
        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'data': data,
            'docs': self.env['account.move'].browse(docids),
        }