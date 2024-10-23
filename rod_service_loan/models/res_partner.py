from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    loan_service_ids = fields.One2many('service.loan', 'partner_id', string='Préstamos')


    @api.depends('loan_service_ids')
    def compute_loan_count(self):
        for partner in self:
            partner.loan_count = len(partner.loan_service_ids)

    def init_loan_service(self):
        external = self.env['external.partner'].create({
            'name': self.name,
            'name_contact': self.name_contact,
            'paternal_surname': self.paternal_surname,
            'maternal_surname': self.maternal_surname,
            'code_external_contact': self.code_contact,
            'ci': self.vat,
            'mobile': self.mobile,
            'partner_id': self.id,
        })
        if external:
            return {
                'name': _('Contacto externo'),
                'view_mode': 'form',
                'res_model': 'external.partner',
                'type': 'ir.actions.act_window',
                'res_id': external.id,
                'target': 'current',
            }
        else:
            raise UserError('Error al crear el contacto externo')
