from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    interest_rate = fields.Float(string='Tasa de interés', default=0.0)
    loan_max_amount = fields.Float(string='Monto máximo', default=0.0)

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('rod_consumer_loan.interest_rate', self.interest_rate)
        self.env['ir.config_parameter'].set_param('rod_consumer_loan.loan_max_amount', self.loan_max_amount)

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            interest_rate=self.env['ir.config_parameter'].get_param('rod_consumer_loan.interest_rate', default=0.0),
            loan_max_amount=self.env['ir.config_parameter'].get_param('rod_consumer_loan.loan_max_amount', default=0.0)
        )
        return res
