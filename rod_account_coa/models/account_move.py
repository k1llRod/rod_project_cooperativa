from odoo import models, fields, api, _
from odoo.exceptions import UserError
from num2words import num2words

class AccountMove(models.Model):
    _inherit = 'account.move'

    # journal_id = fields.Many2one('account.journal', string='Diario', default=_get_default_journal)
    payroll_payment_id = fields.Many2one('payroll.payments', string='Pago de planilla')
    glosa = fields.Text(string='Glosa')
    literal_number = fields.Char(string='Amount literal', compute='_compute_literal_number')
    loan_application_id = fields.Many2one('loan.application', string='Solicitud de préstamo')
    @api.model
    def _get_default_journal(self):
        ''' Get the default journal.
        It could either be passed through the context using the 'default_journal_id' key containing its id,
        either be determined by the default type.
        '''
        move_type = self._context.get('default_move_type', 'entry')
        if move_type in self.get_sale_types(include_receipts=True):
            journal_types = ['sale']
        elif move_type in self.get_purchase_types(include_receipts=True):
            journal_types = ['purchase']
        else:
            journal_types = self._context.get('default_move_journal_types', ['general'])

        if self._context.get('default_journal_id'):
            journal = self.env['account.journal'].browse(self._context['default_journal_id'])

            if move_type != 'entry' and journal.type not in journal_types:
                raise UserError(_(
                    "Cannot create an invoice of type %(move_type)s with a journal having %(journal_type)s as type.",
                    move_type=move_type,
                    journal_type=journal.type,
                ))
        else:
            journal = self._search_default_journal(journal_types)

        return journal

    journals_ids = fields.Many2one('account.journal', string='Diario contable', required=True, readonly=True,
                                 states={'draft': [('readonly', False)]},
                                 check_company=True,
                                 default=_get_default_journal)
    def wizard_payroll_all(self):
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
    def wizard_loan_all(self):
        context = {
            'default_account_move_id': self.id,
            'default_account_journal_id': self.journal_id.id,
        }
        return {
            'type': 'ir.actions.act_window',
            'name': 'Egresos',
            'res_model': 'wizard.loan',
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
    @api.onchange('journals_ids')
    def _onchange_journals_ids(self):
        if self.journals_ids:
            self.journal_id = self.journals_ids

    @api.model
    def create(self, vals):
        if 'journals_ids' in vals:
            vals['journal_id'] = vals['journals_ids']
        return super(AccountMove, self).create(vals)

    # def action_post(self):
    #     res = super(AccountMove, self).action_post()
    #     a = 1
    #     return res

    def print_account_move(self):
        a = 1
        return self.env.ref('rod_account_coa.action_report_pdf_account_move').report_action(self)

    @api.depends('amount_total')
    def _compute_literal_number(self):
        for record in self:
            record.literal_number = num2words(round(record.amount_total), lang='es').upper()
            decimal = str(round(record.amount_total % 1 * 100))
            record.literal_number= record.literal_number + ', CON ' + decimal + '/100 BOLIVIANOS'
            # record.literal_number = decimal_text

    def update_lines(self):
        for line in self:
            line.line_ids._compute_parcial()
