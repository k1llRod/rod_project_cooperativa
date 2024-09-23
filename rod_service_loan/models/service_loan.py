from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

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
    loan_max_amount = fields.Float(string='Monto máximo de préstamo', required=True, track_visibility='always')
    amount_consumed = fields.Float(string='Monto consumido', compute='_compute_amount_consumed', store=True, track_visibility='always')
    interest_rate = fields.Float(string='Tasa de interés', required=True, track_visibility='always')
    payment_ids = fields.One2many('service.loan.payment', 'loan_id', string='Pagos', track_visibility='always')
    # total_paid = fields.Float(string='Total pagado', compute='_compute_total_paid', store=True, track_visibility='always')
    # total_interest = fields.Float(string='Total de intereses', compute='_compute_total_interest', store=True)
    # total_amount = fields.Float(string='Total a pagar', compute='_compute_total_amount', store=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('approved', 'Aprobado'),
        ('paid', 'Pagado'),
        ('cancel', 'Cancelado'),
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

    def action_confirmation(self):
        self.state = 'approved'
        return True