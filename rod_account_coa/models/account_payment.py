from odoo import models, fields, api, _

class AccountPayment(models.Model):
    _inherit = 'account.payment'
    partner_number_account = fields.Char(string='Número de cuenta socio', related='partner_id.bank_ids.acc_number', store=True)

    # def action_post(self):
    #     res = super(AccountPayment, self).action_post()
    #     for line in self.move_id.line_ids:
    #         line.name = "Ingreso a la cuenta " + self.journal_id.bank_acc_number
    #     return res



