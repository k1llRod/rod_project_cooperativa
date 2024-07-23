from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
import re
from dateutil.relativedelta import relativedelta


class WizardPayroll(models.TransientModel):
    _name = 'wizard.payroll'

    # Campos del wizard
    account_move_id = fields.Many2one('account.move', string='Asiento contable')
    name = fields.Char(string='ID aporte')
    date = fields.Date(string='Fecha', default=fields.Datetime.now())
    period = fields.Char(string='Periodo', compute="compute_period_register")
    state = fields.Selection(
        [('draft', 'Borrador'), ('transfer', 'Transferencia bancaria'), ('ministry_defense', 'Ministerio de defensa'),
         ('contribution_interest', 'Aporte y rendimiento COAA'),
         ('no_contribution', 'Sin aporte'),
         ('capital_initial', 'Capital inicial')],
        default='ministry_defense', string='Estado')
    account_journal_id = fields.Many2one('account.journal', string='Diario')
    payment_date = fields.Date(string='Fecha de pago')
    amount_total = fields.Float(string='Monto total')
    amount_total_contributions = fields.Float(string='Monto total de aportes')
    account_income_id = fields.Many2one('account.account', string='Cuenta de ingreso')
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
                payroll_payment = self.env['payroll.payments'].search([('period_register', '=', record.period),('state','=',record.state)])
                record.total_income = round(sum(self.env['payroll.payments'].search([('period_register', '=', record.period),('state','=',record.state)]).mapped('income')),2)
                record.total_miscellaneous_income = round(sum(self.env['payroll.payments'].search([('period_register', '=', record.period),('partner_status_especific','=','active_service'),('state','=',record.state)]).mapped('miscellaneous_income')),2)
                record.total_regulation_cup = round(sum(self.env['payroll.payments'].search([('period_register', '=', record.period),('partner_status_especific','=','active_service'),('state','=',record.state)]).mapped('regulation_cup')),2)
                record.total_mandatory_contribution = round(sum(self.env['payroll.payments'].search([('period_register', '=', record.period),('partner_status_especific','=','active_service'),('state','=',record.state)]).mapped('mandatory_contribution_certificate')),2)
                record.total_voluntary_contribution = round(sum(self.env['payroll.payments'].search([('period_register', '=', record.period),('partner_status_especific','=','active_service'),('state','=',record.state)]).mapped('voluntary_contribution_certificate')),2)
                record.amount_total = record.total_miscellaneous_income + record.total_regulation_cup + record.total_mandatory_contribution + record.total_voluntary_contribution

    def action_confirm(self):
        move_line = []
        reference = 'TRASPASO DE APORTES ' + self.period
        for record in self:
            journal_id = record.account_journal_id
            data = (0, 0,{
                    'account_id': record.account_income_id.id,
                    'name': record.name,
                    'debit': record.total_income if record.total_income > 0 else 0,
                    'credit': 0
            })
            if not (record.total_income == 0): move_line.append(data)
            data = (0, 0, {
                    'account_id': record.account_inscription_id.id,
                    'name': record.name,
                    'debit': 0,
                    'credit': record.total_miscellaneous_income,
            })
            if not (record.total_miscellaneous_income == 0): move_line.append(data)
            data = (0, 0, {
                    'account_id': record.account_regulation_cup_id.id,
                    'name': record.name,
                    'debit': 0,
                    'credit': record.total_regulation_cup,
            })
            if not (record.total_regulation_cup == 0): move_line.append(data)
            data = (0, 0, {
                    'account_id': record.account_mandatory_contribution_id.id,
                    'name': record.name,
                    'debit': 0,
                    'credit': record.total_mandatory_contribution,
            })
            if not (record.total_mandatory_contribution == 0): move_line.append(data)
            data = (0, 0, {
                    'account_id': record.account_voluntary_contribution_id.id,
                    'name': record.name,
                    'debit': 0,
                    'credit': record.total_voluntary_contribution,
            })
            if not (record.total_voluntary_contribution == 0): move_line.append(data)
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
        search_payments = self.env['payroll.payments'].search([('period_register', '=', record.period),('partner_status_especific','=','active_service'),('state','=','ministry_defense')])
        for payment in search_payments:
            payment.write({'account_move_id': account_move_id.id})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': account_move_id.id,
            'views': [(False, 'form')],
        }



