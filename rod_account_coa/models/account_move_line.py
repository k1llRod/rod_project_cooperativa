from odoo import models, fields, api, _

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    parcial = fields.Float(string='Parcial', compute='_compute_parcial', store=True)

    @api.depends('debit', 'credit')
    def _compute_parcial(self):
        for record in self:
            dollar = round(record.env['res.currency'].search([('name', '=', 'USD')], limit=1).inverse_rate,2)
            record.parcial = round(record.debit / dollar,2) if record.debit > 0 else round(record.credit / dollar,2)