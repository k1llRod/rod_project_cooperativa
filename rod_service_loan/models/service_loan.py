from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class ServiceLoan(models.Model):
    _name = 'service.loan'
    _description = 'Service Loan'
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Codigo prestamo de servicio')
    partner_id = fields.Many2one('res.partner', string='Socio', required=True)
    external_partner_id = fields.Char(string='ID de socio externo')
    code_contact = fields.Char(string='Código de contacto')
    loan_date = fields.Date(string='Fecha de préstamo', required=True)
    loan_max_amount = fields.Float(string='Monto máximo de préstamo', required=True)
    interest_rate = fields.Float(string='Tasa de interés', required=True)
    payment_ids = fields.One2many('service.loan.payment', 'loan_id', string='Pagos')
    total_paid = fields.Float(string='Total pagado', compute='_compute_total_paid', store=True)
    # total_interest = fields.Float(string='Total de intereses', compute='_compute_total_interest', store=True)
    # total_amount = fields.Float(string='Total a pagar', compute='_compute_total_amount', store=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('approved', 'Aprobado'),
        ('paid', 'Pagado'),
        ('cancel', 'Cancelado'),
    ], string='Estado', default='draft', required=True)

    @api.depends('payment_ids.amount')
    def _compute_total_paid(self):
        for record in self:
            record.total_paid = sum(record.payment_ids.mapped('amount'))

    # @api.depends('payment_ids.interest')
    # def _compute_total_interest(self):
    #     for record in self:
    #         record.total_interest = sum(record.payment_ids.mapped('interest'))

    # @api.depends('amount', 'interest_rate', 'payment_ids.amount')
    # def _compute_total_amount(self):
    #     for record in self:
    #         record.total_amount = record.amount + record.total_interest