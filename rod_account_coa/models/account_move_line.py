from odoo import models, fields, api, _

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    parcial = fields.Float(string='Parcial', compute='_compute_parcial', store=True)
    # nro_account = fields.Float(string='Nro. de cuenta', related='account_id.code', store=True)

    @api.depends('debit', 'credit')
    def _compute_parcial(self):
        for record in self:
            dollar = round(record.env['res.currency'].search([('name', '=', 'USD')], limit=1).inverse_rate,2)
            record.parcial = round(record.debit / dollar,2) if record.debit > 0 else round(record.credit / dollar,2)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for record in self:
            label_name = record.partner_id.bank_ids.bank_name if record.partner_id.bank_ids else False
            label_number = record.partner_id.bank_ids.acc_number if record.partner_id.bank_ids else False
            record.name = label_name + ' - ' + label_number if label_name and label_number else False
