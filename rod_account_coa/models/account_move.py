from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    # journal_id = fields.Many2one('account.journal', string='Diario', default=_get_default_journal)
    payroll_payment_id = fields.Many2one('payroll.payments', string='Pago de planilla')
    glosa = fields.Text(string='Glosa')
    def wizard_payroll_all(self):
        a = 1
        context = {
            'default_account_move_id': self.id,
            'default_account_journal_id': self.journal_id.id,
        }
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pagos de planilla',
            'res_model': 'wizard.payroll',
            'view_mode': 'form',
            'target': 'new',
            'context': context,
        }
    def open_payroll_payment_view(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'payroll.payments',
            'view_mode': 'form',
            'res_id': self.payroll_payment_id.id,
            'views': [(False, 'form')],
        }

    # def action_post(self):
    #     res = super(AccountMove, self).action_post()
    #     a = 1
    #     return res
