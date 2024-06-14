from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    # journal_id = fields.Many2one('account.journal', string='Diario', default=_get_default_journal)

    def wizard_payroll_all(self):
        context = {
            'default_account_move_id': self.id,
        }
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pagos de planilla',
            'res_model': 'wizard.payroll',
            'view_mode': 'form',
            'target': 'new',
            'context': context,
        }