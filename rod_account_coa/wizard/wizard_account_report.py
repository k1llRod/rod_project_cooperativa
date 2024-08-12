from odoo import models, fields, api, _


class WizardAccountReport(models.TransientModel):
    _name = 'wizard.account.report'
    _description = 'Wizard Account Report'

    account_move_id = fields.Many2one('account.move', string='Asiento contable')
    name = fields.Char(string='ID aporte')
    date = fields.Date(string='Fecha', default=fields.Datetime.now())
    period = fields.Char(string='Periodo', compute="compute_period_register")
    state = fields.Selection(
        [('draft', 'Borrador'), ('transfer', 'Transferencia bancaria'), ('ministry_defense', 'Ministerio de defensa'),
         ],
        default='ministry_defense', string='Estado')
    account_journal_id = fields.Many2one('account.journal', string='Diario')


    def action_confirm(self):
        a = 1