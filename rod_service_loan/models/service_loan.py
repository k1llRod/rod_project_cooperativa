import calendar
from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

class ServiceLoan(models.Model):
    _name = 'service.loan'
    _description = 'Service Loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Codigo prestamo de servicio')
    partner_id = fields.Many2one('res.partner', string='Socio')
    external_partner_id = fields.Many2one('external.partner', string='Solicitante externo')
    name_partner = fields.Char(string='Nombre del solicitante', compute='_compute_name_partner', store=True)
    ci_partner = fields.Char(string='C.I.', compute='_compute_name_partner', store=True)
    mobile_partner = fields.Char(string='Movil', compute='_compute_name_partner', store=True)

    # external_partner_id = fields.Char(string='ID de socio externo')
    code_contact = fields.Char(string='Código de contacto')
    loan_date = fields.Date(string='Fecha de préstamo', required=True)
    loan_max_amount = fields.Float(string='Monto máximo de préstamo', default=lambda self: float(self.env['ir.config_parameter'].sudo().get_param('rod_service_loan.loan_max_amount')))
    amount_consumed = fields.Float(string='Monto consumido', compute='_compute_amount_consumed', store=True, track_visibility='always')
    interest_rate = fields.Float(string='Tasa de interés', default=lambda self: float(
        self.env['ir.config_parameter'].sudo().get_param('rod_service_loan.interest_rate')))
    payment_ids = fields.One2many('service.loan.payment', 'loan_id', string='Pagos', track_visibility='always')
    payment_loan_ids = fields.One2many('payment.loan', 'service_loan_id', string='Pagos de prestamo', track_visibility='always')

    months_quantity = fields.Integer(string='Cantidad de meses', default=1)
    commission_min_def = fields.Float(string='MIND 0.25', default=0.25, digits=(6, 3))
    surplus_days = fields.Integer(string='Dias excedentes')
    monthly_interest = fields.Float(string='Interes mensual')
    interest_month_surpluy = fields.Float(string='Interes mensual excedente')
    capital_month = fields.Float(string='Capital mensual')
    fixed_fee = fields.Float(string='Cuota fija')
    discount_mindef = fields.Float(string='Descuento MINDEF', compute='_compute_total_fee', store=True)

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('approved', 'Aprobado'),
        ('paid', 'Pagado'),
        ('cancel', 'Cancelado'),
        ('rejected','Rechazado'),
    ], string='Estado', default='draft', required=True, track_visibility='always')

    @api.depends('payment_ids')
    def _compute_total_paid(self):
        for record in self:
            record.total_paid = sum(record.payment_ids.filtered(lambda x:x.state == 'confirm' or x.state == 'paid').mapped('amount'))

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('service.loan')
        return super(ServiceLoan, self).create(vals)

    @api.depends('payment_ids')
    def _compute_amount_consumed(self):
        for record in self:
            record.amount_consumed = sum(record.payment_ids.filtered(lambda x:x.state == 'confirm' or x.state == 'paid').mapped('amount'))

    @api.depends('partner_id', 'external_partner_id')
    def _compute_name_partner(self):
        for record in self:
            if record.partner_id:
                record.name_partner = record.partner_id.name
                record.ci_partner = record.partner_id.ci
                record.mobile_partner = record.partner_id.mobile
            if record.external_partner_id:
                record.name_partner = record.external_partner_id.name
                record.ci_partner = record.external_partner_id.ci
                record.mobile_partner = record.external_partner_id.mobile



    def supplier_payment(self):
        for record in self:
            action = record.env['payment.loan'].create({
                'service_loan_id': record.id,
                'amount': record.fixed_fee,
                'interest': record.monthly_interest,
                'payment_date': datetime.today(),
                'discount_mindef': record.fixed_fee + record.monthly_interest,
                'state': 'confirm'
            })
        return action

    def action_confirmation(self):
        self.calculate_surplus_days()
        action = self.supplier_payment()
        if action:
            self.state = 'approved'
        else:
            raise UserError('Error al confirmar el prestamo')
    def calculate_surplus_days(self):
        for record in self:
            try:
                if record.loan_date:
                    interest_rate = round((record.interest_rate) / 1000, 3)
                    last_day = calendar.monthrange(record.loan_date.year, record.loan_date.month)[1]
                    point_day = last_day - record.loan_date.day
                    record.surplus_days = point_day
                    calculte_interest = round(record.amount_consumed * (interest_rate))
                    if record.months_quantity > 0:
                        record.fixed_fee = record.amount_consumed * interest_rate / (
                                    1 - (1 + interest_rate) ** -record.months_quantity)
                    if record.amount_consumed > 0:
                        record.interest_month_surpluy = (calculte_interest / last_day) * (
                                point_day / record.months_quantity)
                        record.monthly_interest = calculte_interest
                        record.capital_month = round(record.fixed_fee, 2) - record.monthly_interest
                else:
                    record.surplus_days = 0
                    record.interest_month_surpluy = 0
            except Exception as e:
                return 0



    @api.depends('fixed_fee', 'interest_month_surpluy')
    def _compute_total_fee(self):
        for record in self:
            record.discount_mindef = record.fixed_fee + record.monthly_interest
    def action_cancel(self):
        self.state = 'cancel'
        return True

    def action_draft(self):
        self.state = 'draft'
        return True

    def action_paid(self):
        self.state = 'paid'
        return True

    def action_rejected(self ):
        self.state = 'rejected'
        return True