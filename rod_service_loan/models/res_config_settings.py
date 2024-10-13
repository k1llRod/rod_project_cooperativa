from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    interest_rate = fields.Float(string='Tasa de interés', digits=(6, 2))
    loan_max_amount = fields.Float(string='Monto máximo', digits=(6, 2))

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            interest_rate=float(
                self.env['ir.config_parameter'].sudo().get_param('rod_service_loan.interest_rate')),
            loan_max_amount=float(
                self.env['ir.config_parameter'].sudo().get_param('rod_service_loan.loan_max_amount')),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('rod_service_loan.interest_rate', self.interest_rate)
        self.env['ir.config_parameter'].sudo().set_param('rod_service_loan.loan_max_amount', str(self.loan_max_amount))


