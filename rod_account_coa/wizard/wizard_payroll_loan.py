from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
import re
from dateutil.relativedelta import relativedelta


class WizardPayroll(models.TransientModel):
    _name = 'wizard.payroll.loan'

    # Campos del wizard
    account_move_id = fields.Many2one('account.move', string='Asiento contable')
    name = fields.Char(string='ID aporte')
    date = fields.Date(string='Fecha', default=fields.Datetime.now())
    period = fields.Char(string='Periodo', compute="compute_period_register")
    account_journal_id = fields.Many2one('account.journal', string='Diario')
    amount_total = fields.Float(string='Monto total')
    amount_total_contributions = fields.Float(string='Monto total de prestamo')
    account_income_id = fields.Many2one('account.account', string='Amortizacion prestamo regular')
    account_inscription_id = fields.Many2one('account.account', string='Cuenta de inscripción')
    account_regulation_cup_id = fields.Many2one('account.account', string='Cuenta de regulación de taza')
    account_mandatory_contribution_id = fields.Many2one('account.account', string='Cuenta de aporte obligatorio')
    account_voluntary_contribution_id = fields.Many2one('account.account', string='Cuenta de aporte voluntario')
    total_income = fields.Float(string='Total de ingresos')
    total_miscellaneous_income = fields.Float(string='Total de ingresos varios')
    total_regulation_cup = fields.Float(string='Total de regulación de taza')
    total_mandatory_contribution = fields.Float(string='Total de aporte obligatorio')
    total_voluntary_contribution = fields.Float(string='Total de aporte voluntario')


    @api.depends('date')
    def compute_period_register(self):
        for record in self:
            record.period = record.date.strftime('%m') + '/' + record.date.strftime('%Y')
            if record.period:
                payroll_payment = self.env['payroll.payments'].search([('period_register', '=', record.period)])
                record.total_income = round(sum(self.env['payroll.payments'].search([('period_register', '=', record.period)]).mapped('income')),2)
                record.total_miscellaneous_income = round(sum(self.env['payroll.payments'].search([('period_register', '=', record.period),('partner_status_especific','=','active_service')]).mapped('miscellaneous_income')),2)
                record.total_regulation_cup = round(sum(self.env['payroll.payments'].search([('period_register', '=', record.period),('partner_status_especific','=','active_service')]).mapped('regulation_cup')),2)
                record.total_mandatory_contribution = round(sum(self.env['payroll.payments'].search([('period_register', '=', record.period),('partner_status_especific','=','active_service')]).mapped('mandatory_contribution_certificate')),2)
                record.total_voluntary_contribution = round(sum(self.env['payroll.payments'].search([('period_register', '=', record.period),('partner_status_especific','=','active_service')]).mapped('voluntary_contribution_certificate')),2)
                record.amount_total = record.total_miscellaneous_income + record.total_regulation_cup + record.total_mandatory_contribution + record.total_voluntary_contribution

    def action_confirm(self):
        for record in self:
            record.account_move_id.write({
                'line_ids': [(0, 0, {
                    'account_id': record.account_income_id.id,
                    'name': record.name,
                    'debit': record.total_income if record.total_income > 0 else 0,
                    'credit': 0,
                }),
                (0, 0, {
                    'account_id': record.account_inscription_id.id,
                    'name': record.name,
                    'debit': 0,
                    'credit': record.total_miscellaneous_income,
                }),
                (0, 0, {
                    'account_id': record.account_regulation_cup_id.id,
                    'name': record.name,
                    'debit': 0,
                    'credit': record.total_regulation_cup,
                }),
                (0, 0, {
                    'account_id': record.account_mandatory_contribution_id.id,
                    'name': record.name,
                    'debit': 0,
                    'credit': record.total_mandatory_contribution,
                }),
                (0, 0, {
                    'account_id': record.account_voluntary_contribution_id.id,
                    'name': record.name,
                    'debit': 0,
                    'credit': record.total_voluntary_contribution,
                }),
                ]
            })

