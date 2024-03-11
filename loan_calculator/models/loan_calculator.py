import calendar
from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from collections import OrderedDict

class LoanCalculator(models.Model):
    _name = 'loan.calculator'

    name = fields.Char(string='Codigo de refinancimiento', default='Nuevo')
    amount_loan = fields.Float(string='Monto de prestamo (Bolivianos)', compute='_compute_change_dollars_bolivian')
    amount_loan_dollars = fields.Float(string='Monto de prestamo (dolares)')
    months_quantity = fields.Integer(string='Cantidad de meses')

    amount_loan_max = fields.Float(string='Monto maximo de prestamo (Bolivianos)', compute='_compute_set_amount')
    amount_loan_max_dollars = fields.Float(string='Monto maximo de prestamo (dolares)', )

    surplus_days = fields.Integer(string='Dias excedentes')
    interest_month_surpluy = fields.Float(string='Interes dias excedente')
    total_interest_month_surpluy = fields.Float(string='Total interes mensual excedente',
                                                compute='_compute_total_interest_month_surpluy', store=True)
    date_application = fields.Date(string='Fecha de solicitud', default=fields.Date.today())
    date_approval = fields.Date(string='Fecha de aprobacion')
    with_guarantor = fields.Selection(string='Tipo de prestamo regular',
                                      selection=[('loan_guarantor', 'Prestamo regular'),
                                                 ('mortgage', 'Prestamo hipotecario')])

    mount = fields.Float(string='Cuota fija')
    fixed_fee = fields.Float(string='Cuota fija ($)', compute='_compute_index_loan_fixed_fee')
    fixed_fee_bs = fields.Float(string='Cuota fija (Bs)', compute='_compute_index_loan_fixed_fee_bs')
    index_loan = fields.Float(string='Indice de prestamo ($)', compute='_compute_index_loan_fixed_fee')
    index_loan_bs = fields.Float(string='Indice de prestamo (Bs)')
    pay_slip_balance = fields.Float(string='Saldo boleta de pago')

    contingency_fund = fields.Float(string='Fondo de contingencia %', default=lambda self: float(
        self.env['ir.config_parameter'].sudo().get_param('rod_cooperativa.contingency_fund')))
    monthly_interest = fields.Float(string='Indice de prestamo por mes %', default=lambda self: float(
        self.env['ir.config_parameter'].sudo().get_param('rod_cooperativa.monthly_interest')))
    amount_min_def = fields.Float(string='Min. Defensa %', default=lambda self: float(
        self.env['ir.config_parameter'].sudo().get_param('rod_cooperativa.percentage_min_def')), digits=(6, 3))
    commission_min_def = fields.Float(string='Comision Min. Defensa %', default=lambda self: float(
        self.env['ir.config_parameter'].sudo().get_param('rod_cooperativa.percentage_commission_min_def')),
                                      digits=(6, 3))
    amount_total = fields.Float(string='D/MINDEF $', digits=(16, 2))
    amount_total_bs = fields.Float(string='D/MINDEF Bs', compute='_change_amount_total_bs', digits=(16, 2), store=True)
    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.company.currency_id)
    currency_id_dollar = fields.Many2one('res.currency', string='Moneda en Dólares',
                                         default=lambda self: self.env.ref('base.USD'))
    percentage_amount_min_def = fields.Float(string='%MINDEF', digits=(16, 2), store=True)

    def _compute_set_dollar(self):
        dollar = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        return round(dollar.inverse_rate, 2)
    value_dolar = fields.Float(default=_compute_set_dollar)
    contingency_fund = fields.Float(string='Fondo de contingencia %', default=lambda self: float(
        self.env['ir.config_parameter'].sudo().get_param('rod_cooperativa.contingency_fund')))

    monthly_interest_mortgage = fields.Float(string='Indice de prestamo hipotecario por mes %',
                                             default=lambda self: float(
                                                 self.env['ir.config_parameter'].sudo().get_param(
                                                     'rod_cooperativa.monthly_interest_mortgage')), digits=(6, 3))
    mortgage_loan = fields.Float(string='Prestamo hipotecario %', default=lambda self: float(
        self.env['ir.config_parameter'].sudo().get_param('rod_cooperativa.mortgage_loan')))
    @api.onchange('month_refinance','amount_refinance')
    def _compute_index_loan_fixed_fee(self):
        try:
            interest = (self.monthly_interest + self.contingency_fund) / 100
            index_quantity = (1 - (1 + interest) ** (-self.month_refinance))
            self.index_loan = interest / index_quantity if index_quantity != 0 else 0
            self.fixed_fee = self.amount_refinance * self.index_loan
        except:
            self.index_loan = 0


    @api.depends('amount_refinance','flag_expansion')
    def _compute_amount_delivered(self):
        for rec in self:
            if rec.flag_expansion == False:
                rec.amount_delivered = rec.amount_refinance - rec.capital_rest - rec.interest_days_rest
            else:
                rec.amount_delivered = rec.amount_refinance - rec.capital_rest

    @api.depends('amount_loan_dollars')
    def _compute_change_dollars_bolivian(self):
        for rec in self:
            rec.amount_loan = rec.amount_loan_dollars * rec.value_dolar
            rec.total_interest_month_surpluy = rec.interest_month_surpluy * rec.months_quantity
            rec.percentage_amount_min_def = rec.fixed_fee * rec.amount_min_def
            rec.amount_total = round(rec.fixed_fee, 2) + round(rec.percentage_amount_min_def, 2) + round(
                rec.interest_month_surpluy, 2)
            rec.fixed_fee = rec.amount_loan_dollars * rec.index_loan
            rec.pay_slip_balance = rec.fixed_fee_bs * (100 / 40)

    @api.onchange('months_quantity', 'with_guarantor')
    def _compute_index_loan_fixed_fee(self):
        try:
            if self.with_guarantor == 'loan_guarantor' or self.with_guarantor == 'no_loan_guarantor':
                interest = (self.monthly_interest + self.contingency_fund) / 100
                index_quantity = (1 - (1 + interest) ** (-self.months_quantity))
                self.index_loan = interest / index_quantity if index_quantity != 0 else 0
                self.fixed_fee = self.amount_loan_dollars * self.index_loan
                self.pay_slip_balance = self.fixed_fee_bs * (100 / 40)
            else:
                interest = (self.monthly_interest_mortgage + self.mortgage_loan) / 100
                index_quantity = (1 - (1 + interest) ** (-self.months_quantity))
                self.index_loan = interest / index_quantity if index_quantity != 0 else 0
                self.fixed_fee = self.amount_loan_dollars * self.index_loan
                self.pay_slip_balance = self.fixed_fee_bs * (100 / 40)
        except:
            self.index_loan = 0

    @api.onchange('date_approval')
    def _compute_surplus_days(self):
        for record in self:
            if record.date_approval:
                if record.with_guarantor == 'loan_guarantor':
                    last_day = calendar.monthrange(record.date_approval.year, record.date_approval.month)[1]
                    point_day = last_day - record.date_approval.day
                    record.surplus_days = point_day
                    calculte_interest = record.amount_loan_dollars * (
                                (record.monthly_interest + record.contingency_fund) / 100)
                    record.interest_month_surpluy = (calculte_interest / last_day) * (
                                point_day / record.months_quantity)
                else:
                    last_day = calendar.monthrange(record.date_approval.year, record.date_approval.month)[1]
                    point_day = last_day - record.date_approval.day
                    record.surplus_days = point_day
                    calculte_interest = record.amount_loan_dollars * (
                                (record.monthly_interest_mortgage + record.mortgage_loan) / 100)
                    record.interest_month_surpluy = (calculte_interest / last_day) * (
                            point_day / record.months_quantity)
            else:
                record.surplus_days = 0
                record.interest_month_surpluy = 0

    @api.depends('fixed_fee')
    def _compute_index_loan_fixed_fee_bs(self):
        for rec in self:
            rec.fixed_fee_bs = rec.fixed_fee * rec.value_dolar


    @api.onchange('amount_loan_dollars')
    def _onchange_amount_loan_dollars(self):
        self.fixed_fee = self.amount_loan_dollars * self.index_loan
        self.pay_slip_balance = self.fixed_fee_bs * (100 / 40)


    @api.onchange('amount_total')
    def _change_amount_total_bs(self):
        for rec in self:
            rec.amount_total_bs = rec.amount_total * rec.currency_id_dollar.inverse_rate

    @api.depends('interest_month_surpluy', 'months_quantity')
    def _compute_total_interest_month_surpluy(self):
        for rec in self:
            rec.total_interest_month_surpluy = rec.interest_month_surpluy * rec.months_quantity
            rec.percentage_amount_min_def = rec.fixed_fee * rec.amount_min_def
            rec.amount_total = round(rec.fixed_fee, 2) + round(rec.percentage_amount_min_def, 2) + round(
                rec.interest_month_surpluy, 2)

    def button_value_dolar(self):
        dollar = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        self.value_dolar = round(dollar.inverse_rate, 2)

    def reset_values(self):
        for rec in self:
            rec.amount_loan_dollars = 0
            rec.months_quantity = 0
            rec.months_quantity = 0
            rec.date_approval = False
            rec.interest_month_surpluy = 0
            rec.amount_total = 0

