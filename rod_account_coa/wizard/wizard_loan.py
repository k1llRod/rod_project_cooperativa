from odoo import models, fields, api, _


class WizardLoan(models.TransientModel):
    _name = 'wizard.loan'
    _description = 'Wizard Loan'

    account_move_id = fields.Many2one('account.move', string='Asiento contable')
    name = fields.Char(string='ID aporte')
    date = fields.Date(string='Fecha', default=fields.Datetime.now())
    period = fields.Char(string='Periodo', compute="compute_period_register")
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
    total_income = fields.Float(string='Total de ingresos', digits=(12, 2))
    # total_income_bolivianos = fields.Float(string='Total de ingresos en bolivianos')
    total_capital_index = fields.Float(string='Total cuenta de capital', digits=(12, 2))
    total_capital_index_bolivianos = fields.Float(string='Total cuenta de capital en bolivianos', digits=(12, 2))
    total_interest_base = fields.Float(string='Total interes 0.7%', digits=(12, 2))
    total_interest_base_bolivianos = fields.Float(string='Total interes 0.7% en bolivianos', digits=(12, 2))
    total_res_social = fields.Float(string='Total fondo contingencia', digits=(12, 2))
    total_res_social_bolivianos = fields.Float(string='Total fondo contingencia en bolivianos', digits=(12, 2))
    total_percentage_mindef = fields.Float(string='Total de aporte voluntario', digits=(12, 2))
    total_percentage_mindef_bolivianos = fields.Float(string='Total de aporte voluntario en bolivianos', digits=(12, 2))
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


    @api.depends('date', 'state')
    def compute_period_register(self):
        for record in self:
            dollar = 6.96
            record.period = record.date.strftime('%m') + '/' + record.date.strftime('%Y')
            if record.period:
                loan_payment = self.env['loan.payment'].search([('period', '=', record.period), ('state', '=', record.state)])
                record.total_income = round(sum(loan_payment.mapped('amount_total_bs')), 2)
                record.total_capital_index = round(sum(loan_payment.mapped('capital_index_initial')), 2)
                record.total_interest_base = round(sum(loan_payment.mapped('interest_base')), 2)
                record.total_res_social = round(
                    sum(loan_payment.mapped('res_social')), 2)
                record.total_percentage_mindef = round(
                    sum(loan_payment.mapped('percentage_amount_min_def')), 2)
                record.total_surpluy_days = round(
                    sum(loan_payment.mapped('interest_month_surpluy')), 2)
                record.amount_total = record.total_capital_index + record.total_interest_base + record.total_res_social + record.total_percentage_mindef + record.total_surpluy_days
                record.total_capital_index_bolivianos = record.total_capital_index * dollar
                record.total_interest_base_bolivianos = record.total_interest_base * dollar
                record.total_res_social_bolivianos = record.total_res_social * dollar
                record.total_percentage_mindef_bolivianos = record.total_percentage_mindef * dollar
                record.total_surpluy_days_bolivianos = record.total_surpluy_days * dollar
                record.amount_total_bolivianos = record.total_capital_index_bolivianos + record.total_interest_base_bolivianos + record.total_res_social_bolivianos + record.total_percentage_mindef_bolivianos + record.total_surpluy_days_bolivianos

    @api.onchange('total_capital_index_bolivianos','total_interest_base_bolivianos','total_res_social_bolivianos','total_percentage_mindef_bolivianos','total_surpluy_days_bolivianos')
    def _onchange_mounts(self):
        for record in self:
            record.amount_total_bolivianos = record.total_capital_index_bolivianos + record.total_interest_base_bolivianos + record.total_res_social_bolivianos + record.total_percentage_mindef_bolivianos + record.total_surpluy_days_bolivianos