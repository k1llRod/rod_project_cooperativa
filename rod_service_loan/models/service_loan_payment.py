from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class ServiceLoanPayment(models.Model):
    _name = 'service.loan.payment'
    _description = 'Service Loan Payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Codigo')
    loan_id = fields.Many2one('service.loan', string='Préstamo', required=True, track_visibility='always')
    date = fields.Date(string='Fecha', required=True, track_visibility='always')
    detail = fields.Char(string='Detalle', required=True, track_visibility='always')
    amount = fields.Float(string='Monto', required=True, track_visibility='always')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirm','Confirmado'),
        ('paid', 'Pagado'),
        ('cancel', 'Cancelado'),
    ], string='Estado', default='draft', track_visibility='always')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('service.loan.payment')
        vals['state'] = 'confirm'
        return super(ServiceLoanPayment, self).create(vals)


    def action_confirm(self):
        self.write({})
        self.state = 'confirm'

    def action_draft(self):
        self.state = 'draft'
        return True

    def open_service_loan_payment(self):
        return {
            'name': _('Pago de préstamo de servicio'),
            'view_mode': 'form',
            'res_id': self.id,
            'res_model': 'service.loan.payment',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }