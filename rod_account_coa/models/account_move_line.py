from odoo import models, fields, api, _

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    parcial = fields.Float(string='Parcial', compute='_compute_parcial', store=True)

    @api.depends('debit', 'credit')
    def _compute_parcial(self):
        for record in self:
            record.parcial = record.debit - record.credit