from odoo import models, fields, api, _

class AccountPayment(models.Model):
    _inherit = 'account.payment'
    partner_number_account = fields.Char(string='Número de cuenta socio', related='partner_id.bank_ids.acc_number', store=True)

    # def action_post(self):
    #     res = super(AccountPayment, self).action_post()
    #     for line in self.move_id.line_ids:
    #         if line.account_id.id == line.journal_id.default_debit_account_id.id:
    #             line.name = line.journal_id.bank_account_id
    #     return res



