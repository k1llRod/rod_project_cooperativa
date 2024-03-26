import calendar
from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


class LoanApplicationEmergency(models.Model):
    _name = 'loan.application.emergency'
    _description = 'Loan Application Emergency'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Codigo')
    partner_id = fields.Many2one('res.partner', string='Solicitante')
    code_contact = fields.Char(string='Codigo de socio', related='partner_id.code_contact', store=True)
    category_partner = fields.Char(string='Grado', related='partner_id.category_partner_id.name', store=True)
    ci_partner = fields.Char(string='Carnet de identidad', related='partner_id.vat', store=True)
    partner_status_especific = fields.Selection([('active_service', 'Servicio activo'),
                                                 ('letter_a', 'Letra "A" de disponibilidad'),
                                                 ('passive_reserve_a', 'Reserva pasivo "A"'),
                                                 ('passive_reserve_b', 'Reserva pasivo "B"'),
                                                 ('emergency_military', 'Prestamo emergencia militar'),
                                                 ('emergency_civil', 'Prestamo emergencia civil'),
                                                 ('leave', 'Baja')], string='Tipo de asociado',
                                                related='partner_id.partner_status_especific', store=True)
    amount = fields.Float(string='Monto de prestamo')
    months_quantity = fields.Integer(string='Cantidad de meses')
    interest_rate = fields.Float(string='Tasa de interes', default=0.03, digits=(6, 3))
    date = fields.Date(string='Fecha de prestamo', default=fields.Date.context_today)
    state = fields.Selection([('draft', 'Borrador'), ('approved', 'Aprobado'), ('rejected', 'Rechazado')], string='Estado', default='draft')
    guarantor_one = fields.Many2one('res.partner', string='Garante 1', tracking=True)
    code_garantor_one = fields.Char(string='Codigo de garante 1', related='guarantor_one.code_contact', store=True)

    surplus_days = fields.Integer(string='Dias excedentes')
    surplus_amount = fields.Float(string='Monto excedente')
    global_interest = fields.Float(string='Interes global')
    monthly_interest = fields.Float(string='Interes mensual')

    interest_month_surpluy = fields.Float(string='Interes mensual excedente')
    capital_month = fields.Float(string='Capital mensual')


    commission_min_def = fields.Float(string='Comision Min. Defensa %', default=0.25,
                                      digits=(6, 3))

    # letter_of_request = fields.Boolean(string='Carta de solicitud', tracking=True)
    # contact_request = fields.Boolean(string='Solicitud de prestamo', tracking=True)
    last_copy_paid_slip = fields.Boolean(string='Ultima copia de boleta de pago', tracking=True)
    ci_photocopy = fields.Boolean(string='Fotocopia de CI', tracking=True)
    # photocopy_military_ci = fields.Boolean(string='Fotocopia de Carnet militar', tracking=True)

    fixed_fee = fields.Float(string='Cuota fija')
    ballot_balance = fields.Float(string='Saldo de boleta')
    current_ballot_balance = fields.Float(string='Saldo actual de boleta')
    loan_payment_ids = fields.One2many('loan.payment.emergency', 'loan_application_ids', string='Pagos')

    @api.model
    def create(self, vals):
        name = self.env['ir.sequence'].next_by_code('loan.application.emergency')
        vals['name'] = name
        res = super(LoanApplicationEmergency, self).create(vals)
        return res

    @api.onchange('amount', 'months_quantity', 'interest_rate')
    def _onchange_amount(self):
        if self.months_quantity > 0:
            self.fixed_fee = self.amount * self.interest_rate / (1 - (1 + self.interest_rate) ** -self.months_quantity)

    @api.onchange('date','amount','months_quantity','interest_rate')
    def _compute_surplus_days(self):
        for record in self:
            try:
                if record.date:
                    last_day = calendar.monthrange(record.date.year, record.date.month)[1]
                    point_day = last_day - record.date.day
                    record.surplus_days = point_day
                    calculte_interest = round(record.amount * (record.interest_rate))
                    record.interest_month_surpluy = (calculte_interest / last_day) * (
                                    point_day / record.months_quantity)
                    record.monthly_interest = calculte_interest
                    record.capital_month = record.fixed_fee - record.monthly_interest
                else:
                    record.surplus_days = 0
                    record.interest_month_surpluy = 0
            except Exception as e:
                return 0

    def approve_loan_emergency(self):
        if self.loan_payment_ids: raise ValidationError('Se tienen registros, primero deben ser eliminados.')
        for rec in self:
            if rec.ci_photocopy == False: raise ValidationError('Falta solicitud de prestamo')
            # if rec.letter_of_request == False: raise ValidationError('Falta carta de solicitud')
            if rec.last_copy_paid_slip == False: raise ValidationError('Falta ultima copia de boleta de pago')

            for i in range(1, rec.months_quantity + 1):
                date = rec.date + relativedelta(months=i)
                commission = (round(rec.fixed_fee,2) + round(rec.interest_month_surpluy,2)) * (rec.commission_min_def / 100)
                if len(rec.loan_payment_ids) == 0:
                    capital_init = rec.amount
                    # date_payment = datetime.today()
                    date_payment = rec.date
                    date_pivot = date_payment
                    date_payment = date_payment.replace(day=1)
                    date_payment = date_payment.replace(
                        month=date_payment.month + 1 if date_pivot.month < 12 else 1)
                    date_payment = date_payment.replace(
                        year=date_payment.year + 1 if date_pivot.month == 12 else date_payment.year)
                    capital_index_initial = rec.fixed_fee - rec.monthly_interest
                    capital_balance = capital_init - capital_index_initial
                    interest = rec.monthly_interest
                    capital = rec.capital_month
                else:
                    capital_init = rec.loan_payment_ids[i - 2].capital_balance
                    date_payment = rec.loan_payment_ids[i - 2].date
                    date_payment = date_payment + relativedelta(months=+1)
                    date_payment = date_payment.replace(day=1)
                    interest = capital_init * rec.interest_rate
                    capital = rec.fixed_fee - interest
                    capital_balance = capital_init - capital

                action = self.env['loan.payment.emergency'].create({
                    'name': 'Cuota ' + str(i),
                    'date': date_payment,
                    'capital_index_initial': capital_index_initial,
                    'capital_init': capital_init,
                    'capital_month': capital,
                    'monthly_interest': interest,
                    'capital_balance': capital_balance,
                    'fixed_fee': rec.fixed_fee,
                    'interest_month_surpluy': rec.interest_month_surpluy,
                    'commission_min_def': commission,
                    'loan_application_ids': rec.id,
                    # 'commission_min_def': amount_commission,
                    'state': 'draft',
                })
                action.compute_min_def()

        # self.write({'state': 'approved'})

    def reset_payroll(self):
        for rec in self:
            rec.loan_payment_ids.unlink()
            rec.state = 'draft'

    def return_draft(self):
        self.state = 'draft'

    def approve_loan(self):
        for rec in self:
            rec.state = 'approved'

    def reject_loan(self):
        for rec in self:
            rec.state ='rejected'