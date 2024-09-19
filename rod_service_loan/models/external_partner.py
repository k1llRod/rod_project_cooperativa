from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class ExternalPartner(models.Model):
    _name = 'external.partner'
    _description = 'External Partner'
    _inherit=['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre')
    name_contact = fields.Char(string='Nombres', require=True)
    paternal_surname = fields.Char(string='Apellido paterno')
    maternal_surname = fields.Char(string='Apellido materno')
    code_external_contact = fields.Char(string='Código', required=True)
    ci = fields.Char(string='C.I.', required=True)
    mobile = fields.Char(string='Movil')
    state = fields.Selection([
        ('Activo', 'Activo'),
        ('Rechazado', 'Rechazado'),
    ], string='Estado', default='active', required=True)
    # loan_ids = fields.One2many('service.loan', 'external_partner_id', string='Préstamos')
    # total_loans = fields.Integer(string='Total de préstamos', compute='_compute_total_loans', store=True)

    @api.onchange('name_contact', 'paternal_surname', 'maternal_surname')
    def _onchange_name(self):
        for partner in self:
            if partner.name_contact:
                partner.name = partner.name_contact
            if partner.maternal_surname:
                partner.name = partner.maternal_surname + ' ' + partner.name
            if partner.paternal_surname:
                partner.name = partner.paternal_surname + ' ' + partner.name
            if not partner.name_contact and not partner.paternal_surname and not partner.maternal_surname:
                partner.name = ''

    def enable_loan(self):
        service_loan = self.env['service.loan'].create({
            # 'partner_id': self.id,
            'external_partner_id': self.id,
            'code_contact': self.code_external_contact,
            'loan_date': datetime.now(),
            'loan_max_amount': 0,
            'interest_rate': 0,
            'state': 'draft',
        })
        return {
            'name': _('Préstamo de servicio'),
            'view_mode': 'form',
            'res_id': service_loan.id,
            'res_model': 'service.loan',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('external.partner')
        return super(ExternalPartner, self).create(vals)


    # @api.depends('loan_ids')
    # def _compute_total_loans(self):
    #     for record in self:
    #         record.total_loans = len(record.loan_ids)