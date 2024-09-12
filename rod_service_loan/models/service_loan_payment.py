from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class ServiceLoanPayment(models.Model):
    _name = 'service.loan.payment'
    _description = 'Service Loan Payment'

    name = fields.Char(string='Codigo pago de préstamo de servicio')
    loan_id = fields.Many2one('service.loan', string='Préstamo', required=True)
    date = fields.Date(string='Fecha', required=True)
    amount = fields.Float(string='Monto', required=True)
    total = fields.Float(string='Total', compute='_compute_total', store=True)

    @api.constrains('amount', 'interest')
    def _check_amount(self):
        for record in self:
            if record.amount < 0:
                raise ValidationError(_('El monto del pago no puede ser negativo'))
            if record.interest < 0:
                raise ValidationError(_('El interés del pago no puede ser negativo'))