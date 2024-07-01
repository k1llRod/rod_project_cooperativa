from odoo import models, fields, api, _

class AccountPaymentCoa(models.Model):
    _name = 'account.payment.coa'
    _description = 'Pagos de planilla'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre', required=True)
    date = fields.Date(string='Fecha', required=True)
    amount = fields.Float(string='Monto', required=True)
    payment_type = fields.Selection([('outbound', 'Enviar'), ('inbound','Recibir')], string='Tipo de pago', required=True, default='outbound')
    partner_id = fields.Many2one('res.partner', string='Socio', required=True)
    account_id = fields.Many2one('account.account', string='Cuenta', required=True)
    journal_id = fields.Many2one('account.journal', string='Diario', required=True)
    company_id = fields.Many2one('res.company', string='Compañía', required=True, default=lambda self: self.env.company)
    partner_bank_id = fields.Many2one('res.partner.bank', string='Cuenta bancaria')
    is_internal_transfer = fields.Boolean(string='Transferencia interna')

    ref = fields.Char(string='Referencia')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('posted', 'Publicado'),
    ], string='Estado', default='draft', required=True)

    def action_post(self):
        self.state = 'posted'
        move = self.env['account.move'].create({
            'journal_id': self.journal_id.id,
            'date': self.date,
            'ref': self.name,
            'company_id': self.company_id.id,
            'line_ids': [(0, 0, {
                'name': self.name,
                'account_id': self.account_id.id,
                'debit': 0.0,
                'credit': self.amount,
            }), (0, 0, {
                'name': self.name,
                'account_id': self.journal_id.default_account_id.id,
                'debit': self.amount,
                'credit': 0.0,
            })],
        })
        move.action_post()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pagos de planilla',
            'res_model': 'account.payment.coa',
            'view_mode': 'form',
            'target': 'new',
        }

    def action_draft(self):
        self.state = 'draft'
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pagos de planilla',
            'res_model': 'account.payment.coa',
            'view_mode': 'form',
            'target': 'new',
        }

    def action_cancel(self):
        self.state = 'draft'
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pagos de planilla',
            'res_model': 'account.payment.coa',
            'view_mode': 'form',
            'target': 'new',
        }
    def mark_as_sent(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pagos de planilla',
            'res_model': 'account.payment.coa',
            'view_mode': 'form',
            'target': 'new',
        }
    def unmark_as_sent(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pagos de planilla',
            'res_model': 'account.payment.coa',
            'view_mode': 'form',
            'target': 'new',
        }
