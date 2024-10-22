from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class ExternalPartner(models.Model):
    _name = 'external.partner'
    _description = 'External Partner'
    _inherit=['mail.thread', 'mail.activity.mixin']

    code_external_partner = fields.Char(string='Código', required=True)
    name = fields.Char(string='Nombre')
    name_contact = fields.Char(string='Nombres', require=True)
    paternal_surname = fields.Char(string='Apellido paterno')
    maternal_surname = fields.Char(string='Apellido materno')
    code_external_contact = fields.Char(string='Código', required=True)
    ci = fields.Char(string='C.I.', required=True)
    mobile = fields.Char(string='Movil')

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Activo'),
        ('Rechazado', 'Rechazado'),
    ], string='Estado', default='draft')
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
            'loan_max_amount': self.env['ir.config_parameter'].sudo().get_param('rod_service_loan.loan_max_amount'),
            'interest_rate': self.env['ir.config_parameter'].sudo().get_param('rod_service_loan.interest_rate'),
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
    loan_service_ids = fields.One2many('service.loan', 'external_partner_id', string='Préstamos')
    loan_count = fields.Integer(string='Préstamos',compute='compute_loan_count', store=True)

    @api.depends('loan_service_ids')
    def compute_loan_count(self):
        for record in self:
            loans = len(record.env['service.loan'].search([('external_partner_id', '=', record.id)]))
            record.loan_count = loans

    @api.model
    def create(self, vals):
        vals['code_external_partner'] = self.env['ir.sequence'].next_by_code('external.partner')
        return super(ExternalPartner, self).create(vals)

    def action_view_loans(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("rod_service_loan.action_service_loan")
        action['domain'] = [
            ('external_partner_id.id', '=', self.id),
        ]
        return action

    def action_state_active(self):
        self.write({'state': 'active'})

    def action_state_rechazado(self):
        self.write({'state': 'Rechazado'})

    # @api.depends('loan_ids')
    # def _compute_total_loans(self):
    #     for record in self:
    #         record.total_loans = len(record.loan_ids)