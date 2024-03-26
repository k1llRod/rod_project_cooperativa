import calendar
from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

class LoanPaymentEmergency(models.Model):
    _name = 'loan.payment.emergency'
    _description = 'Loan Payment Emergency'

    name = fields.Char(string='Codigo de pago')
    partner_id = fields.Many2one('res.partner', string='Socio', related='loan_application_ids.partner_id', store=True)
    code_contact = fields.Char(string='Codigo de contacto', related='loan_application_ids.code_contact')
    ci_partner = fields.Char(string='Carnet de identidad', related='loan_application_ids.ci_partner')
    loan_application_ids = fields.Many2one('loan.application.emergency', string='Solicitud de prestamo de emergencia', required=True)
    date = fields.Date(string='Fecha de pago', required=True)
    period = fields.Char(string='Periodo', compute='_compute_period',store=True)
    capital_month = fields.Float(string='Capital')
    capital_init = fields.Float(string='Capital inicial')
    capital_index_initial = fields.Float(string='Capital index')
    capital_balance = fields.Float(string='Saldo capital', digits=(16, 2), store=True)
    fixed_fee = fields.Float(string='Cuota fija')
    monthly_interest = fields.Float(string='Interes Mensual', store=True)
    interest = fields.Float(string="Interes")
    interest_month_surpluy = fields.Float(string='Interes mensual excedente')
    commission_min_def = fields.Float(string='Comision Min. Defensa %',
                                      digits=(6, 3))
    payment_mindef = fields.Float(string='Descuento MINDEF')
    state = fields.Selection(
        [('draft', 'Borrador'), ('transfer', 'Transferencia bancaria'),
         ('ministry_defense', 'Ministerio de defensa'), ('debt_settlement_mindef', 'Liquidacion de deuda MINDEF'),
         ('debt_settlement_deposit', 'Liquidacion de deuda por deposito')], string='Estado',
        default='draft', tracking=True)
    # company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    # currency_id = fields.Many2one('res.currency', string='Moneda', related='loan_application_ids.currency_id')
    # currency_id_dollar = fields.Many2one('res.currency', string='Moneda en Dólares',
    #                                      default=lambda self: self.env.ref('base.USD'))

    # @api.depends('capital_initial', 'balance_capital', 'interest', 'res_social')
    # def _compute_interest(self):
    #     percentage_interest = self.loan_application_ids.interest_rate
    #     # interest = (percentage_interest + contingency_found) / 100
    #     for rec in self:
    #         rec.interest = rec.capital_initial * percentage_interest
    #         rec.interest_base = rec.capital_initial * round((percentage_interest / 100), 3)
    #         rec.capital_index_initial = round(rec.mount - rec.interest, 2)
    #
    #         rec.balance_capital = rec.capital_initial - rec.capital_index_initial
    #         rec.amount_total = round(rec.mount, 2) + round(rec.percentage_amount_min_def, 2) + round(
    #             rec.interest_month_surpluy, 2)
    #         rec._change_amount_total_bs()
            # rec.commission_min_def = round((commission_min_def / 100) * rec.amount_total_bs,2)
            # commision_auxiliar = rec.commission_min_def
            # rec.amount_returned_coa = round(rec.amount_total_bs,2) - commision_auxiliar

    @api.depends('date')
    def _compute_period(self):
        for rec in self:
            rec.period = rec.date.strftime('%m/%Y')

    @api.onchange('')

