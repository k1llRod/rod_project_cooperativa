from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class PaymentLoan(models.Model):
    _name = 'payment.loan'
    _description = 'Payment Loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Codigo pago')
    service_loan_id = fields.Many2one('service.loan', string='Prestamo')
    amount = fields.Float(string='Monto', required=True)
    interest = fields.Float(string='Interes', required=True)
    discount_mindef = fields.Float(string='Descuento MINDEF', required=True)
    payment_date = fields.Date(string='Fecha de pago', required=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirm', 'Confirmado'),
        ('paid', 'Pagado'),
        ('cancel', 'Cancelado'),
    ], string='Estado', default='draft', required=True, track_visibility='always')

    # @api.model
    # def create(self, vals):
    #     vals['name'] = self.env['ir.sequence'].next_by_code('payment.loan')
    #     return super(PaymentLoan, self).create(vals)
    #
    # @api.multi
    # def action_confirm(self):
    #     for record in self:
    #         record.state = 'confirm'
    #
    # @api.multi
    # def action_pay(self):
    #     for record in self:
    #         record.state = 'paid'
    #
    # @api.multi
    # def action_cancel(self):
    #     for record in self:
    #         record.state = 'cancel'