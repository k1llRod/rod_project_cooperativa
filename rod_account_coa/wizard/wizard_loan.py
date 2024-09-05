from odoo import models, fields, api, _


class WizardLoan(models.TransientModel):
    _name = 'wizard.loan'
    _description = 'Wizard Loan'

    account_move_id = fields.Many2one('account.move', string='Asiento contable')
    name = fields.Char(string='ID aporte')
    date = fields.Date(string='Fecha', default=fields.Datetime.now())
    period = fields.Char(string='Periodo')
    state = fields.Selection(
        [('draft', 'Borrador'), ('transfer', 'Transferencia bancaria'), ('ministry_defense', 'Ministerio de defensa'),
         ],
        default='ministry_defense', string='Estado')
    account_journal_id = fields.Many2one('account.journal', string='Diario')
    payment_date = fields.Date(string='Fecha de pago', digits=(12, 2))
    amount_total = fields.Float(string='Monto total')
    amount_total_bolivianos = fields.Float(string='Monto total en bolivianos', digits=(12, 2))
    # amount_total_contributions = fields.Float(string='Monto total de aportes', digits=(12, 2))
    account_income_id = fields.Many2one('account.account', string='Cuenta de ingreso')
    account_capital_index_id = fields.Many2one('account.account', string='Cuenta de capital')
    account_interest_base = fields.Many2one('account.account', string='Interes 0.7%')
    account_res_social = fields.Many2one('account.account', string='Fondo por Contingencia 0.04%')
    account_percentage_mindef = fields.Many2one('account.account', string='Porcentaje Min. Defensa')
    account_surpluy_days = fields.Many2one('account.account', string='Interes dias excedentes')
    total_income = fields.Float(string='Total de ingresos', digits=(12, 2), store=True)
    # total_income_bolivianos = fields.Float(string='Total de ingresos en bolivianos')
    total_capital_index = fields.Float(string='Total cuenta de capital', digits=(12, 2))
    total_capital_index_bolivianos = fields.Float(string='Total cuenta de capital en bolivianos', digits=(12, 2))
    total_interest_base = fields.Float(string='Total interes 0.7%', digits=(12, 2))
    total_interest_base_bolivianos = fields.Float(string='Total interes 0.7% en bolivianos', digits=(12, 2))
    total_res_social = fields.Float(string='Total fondo contingencia', digits=(12, 2))
    total_res_social_bolivianos = fields.Float(string='Total fondo contingencia en bolivianos', digits=(12, 2))
    total_percentage_mindef = fields.Float(string='Total porcentaje MINDEF', digits=(12, 2))
    total_percentage_mindef_bolivianos = fields.Float(string='Total porcentaje MINDEF en bolivianos', digits=(12, 2))
    total_surpluy_days = fields.Float(string='Total de dias excedentes', digits=(12, 2))
    total_surpluy_days_bolivianos = fields.Float(string='Total de dias excedentes en bolivianos', digits=(12, 2))

    # @api.depends('amount_total','total_capital_index','total_interest_base','total_res_social','total_percentage_mindef','total_surpluy_days')
    def _amount_total_bolivanos(self):
        for record in self:
            dollar = 6.96
            # record.amount_total_bolivianos = record.amount_total * dollar
            record.total_capital_index_bolivianos = record.total_capital_index * dollar
            record.total_interest_base_bolivianos = record.total_interest_base * dollar
            record.total_res_social_bolivianos = record.total_res_social * dollar
            record.total_percentage_mindef_bolivianos = record.total_percentage_mindef * dollar
            record.total_surpluy_days_bolivianos = record.total_surpluy_days * dollar
            record.amount_total_bolivianos = record.total_capital_index_bolivianos + record.total_interest_base_bolivianos + record.total_res_social_bolivianos + record.total_percentage_mindef_bolivianos + record.total_surpluy_days_bolivianos



    @api.onchange('date', 'state')
    def compute_period_register(self):
        for record in self:
            dollar = 6.96
            record.period = record.date.strftime('%m') + '/' + record.date.strftime('%Y')
            if record.period:
                loan_payment = self.env['loan.payment'].search([('period', '=', record.period), ('state', '=', record.state)])
                record.total_income = round(sum(loan_payment.mapped('amount_returned_coa')), 2)
                record.total_capital_index = round(sum(loan_payment.mapped('capital_index_initial')), 2)
                record.total_interest_base = round(sum(loan_payment.mapped('interest_base')), 2)
                record.total_res_social = round(
                    sum(loan_payment.mapped('res_social')), 2)

                percentage = round(
                    sum(loan_payment.mapped('percentage_amount_min_def')), 2)
                percentage_mindef = round(
                    sum(loan_payment.mapped('commission_min_def')), 2)

                record.total_percentage_mindef = round(
                    sum(loan_payment.mapped('coa_commission')), 2)

                record.total_surpluy_days = round(
                    sum(loan_payment.mapped('interest_month_surpluy')), 2)
                record.amount_total = record.total_capital_index + record.total_interest_base + record.total_res_social + record.total_percentage_mindef + record.total_surpluy_days
                record.total_capital_index_bolivianos = record.total_capital_index * dollar
                record.total_interest_base_bolivianos = record.total_interest_base * dollar
                record.total_res_social_bolivianos = record.total_res_social * dollar
                record.total_percentage_mindef_bolivianos = round(sum(loan_payment.mapped('coa_commission_bs')), 2)
                record.total_surpluy_days_bolivianos = record.total_surpluy_days * dollar
                record.amount_total_bolivianos = record.total_capital_index_bolivianos + record.total_interest_base_bolivianos + record.total_res_social_bolivianos + record.total_percentage_mindef_bolivianos + record.total_surpluy_days_bolivianos

    @api.onchange('total_capital_index_bolivianos','total_interest_base_bolivianos','total_res_social_bolivianos','total_percentage_mindef_bolivianos','total_surpluy_days_bolivianos')
    def _onchange_mounts(self):
        for record in self:
            record.amount_total_bolivianos = record.total_capital_index_bolivianos + record.total_interest_base_bolivianos + record.total_res_social_bolivianos + record.total_percentage_mindef_bolivianos + record.total_surpluy_days_bolivianos


    def action_confirm(self):
        a = 1
        move_line = []
        reference = 'PREST. AMORTIZABLE CORRESP. ' + self.period
        for record in self:
            # reference = record.period
            journal_id = record.account_journal_id
            data = (0, 0, {
                'account_id': record.account_income_id.id,
                # 'name': record.name,
                'debit': record.total_income if record.total_income > 0 else 0,
                'credit': 0
            })
            if not (record.total_income == 0): move_line.append(data)
            data = (0, 0, {
                'account_id': record.account_capital_index_id.id,
                'name': record.name,
                'debit': 0,
                'credit': record.total_capital_index_bolivianos,
            })
            if not (record.total_capital_index_bolivianos == 0): move_line.append(data)
            data = (0, 0, {
                'account_id': record.account_interest_base.id,
                'name': record.name,
                'debit': 0,
                'credit': record.total_interest_base_bolivianos,
            })
            if not (record.total_interest_base_bolivianos == 0): move_line.append(data)
            data = (0, 0, {
                'account_id': record.account_res_social.id,
                'name': record.name,
                'debit': 0,
                'credit': record.total_res_social_bolivianos,
            })
            if not (record.total_res_social_bolivianos == 0): move_line.append(data)
            data = (0, 0, {
                'account_id': record.account_percentage_mindef.id,
                'name': record.name,
                'debit': 0,
                'credit': record.total_percentage_mindef_bolivianos,
            })
            if not (record.total_percentage_mindef_bolivianos == 0): move_line.append(data)
            data = (0, 0, {
                'account_id': record.account_surpluy_days.id,
                'name': record.name,
                'debit': 0,
                'credit': record.total_surpluy_days_bolivianos,
            })
            if not (record.total_surpluy_days_bolivianos == 0): move_line.append(data)
        move_vals = {
            "date": record.payment_date,
            "journal_id": journal_id.id,
            "ref": reference,
            # "company_id": payment.company_id.id,
            # "name": "name test",
            "state": "draft",
            "line_ids": move_line,
        }
        account_move_id = record.env['account.move'].create(move_vals)
        self.account_move_id.unlink()
        search_payments = self.env['loan.payment'].search(
            [('period', '=', record.period),
             ('state', '=', 'ministry_defense')])
        for payment in search_payments:
            payment.write({'account_move_id': account_move_id.id})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': account_move_id.id,
            'views': [(False, 'form')],
        }