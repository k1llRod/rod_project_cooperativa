from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError

class LoanPayment(models.Model):
    _name = 'loan.payment.calculator'
    _description = 'Pagos de prestamos'

    name = fields.Char(string='Codigo de pago', required=True)
    loan_calculator_ids = fields.Many2one('loan.calculator', string='Solicitud de prestamo', required=True)
    # type_loan = fields.Selection([('regular', 'Regular'), ('emergency', 'Emergencia')], string='Tipo de prestamo', related='loan_calculator_ids.type_loan')
    with_guarantor = fields.Selection([('loan_guarantor', 'Prestamo regular con garantes'), ('no_loan_guarantor', 'Prestamo regular sin garantes')], string='Tipo de prestamo regular', related='loan_calculator_ids.with_guarantor')
    # partner_status_especific = fields.Selection([('active_service', 'Servicio activo'), ('guest', 'Invitado'),
    #                                              ('passive_reserve_a','Pasivo categoria "A"'),('passive_reserve_b','Pasivo categoria "B"')
    #                                              ('leave','Baja')], string='Estatus del socio', related='loan_application_ids.partner_status_especific')
    date = fields.Date(string='Fecha de pago', required=True)
    period = fields.Char(string='Periodo', compute='_compute_period', store=True)
    capital_initial = fields.Float(string='Capital inicial')
    capital_index_initial = fields.Float(string='Capital')
    mount = fields.Float(string='Cuota fija')
    interest = fields.Float(string='Interes', compute='_compute_interest', store=True)
    interest_base = fields.Float(string='0.7%', compute='_compute_interest', store=True)
    interest_mortgage = fields.Float(string='Interes H.', compute='_compute_interest', store=True)
    interest_base_mortgage = fields.Float(string='0.207%', compute='_compute_interest', digits=(16, 2),store=True)
    res_social = fields.Float(string='F.C. 0.04%', compute='_compute_interest', digits=(16, 2),store=True)
    res_mortgage = fields.Float(string='P.H. 0.04%', compute='_compute_interest', digits=(16, 2),store=True)
    balance_capital = fields.Float(string='Saldo capital', compute='_compute_interest', digits=(16, 2),store=True)
    percentage_amount_min_def = fields.Float(string='%MINDEF',  digits=(16, 2), store=True)
    commission_min_def = fields.Float(string='0.25% MINDEF', digits=(16, 2), store=True)
    coa_commission = fields.Float(string='Comision COA')
    interest_month_surpluy = fields.Float(string='D/E',  digits=(16, 2), store=True)
    amount_total = fields.Float(string='D/MINDEF $', digits=(16, 2))
    amount_total_bs = fields.Float(string='D/MINDEF Bs', compute='_change_amount_total_bs', digits=(16, 2),store=True)
    amount_returned_coa = fields.Float(string='Monto devuelto COA',digits=(16, 2), store=True)
    state = fields.Selection(
        [('draft', 'Borrador'), ('transfer', 'Transferencia bancaria'),
         ('ministry_defense', 'Ministerio de defensa'), ('debt_settlement_mindef', 'Liquidacion de deuda MINDEF'),
         ('debt_settlement_deposit', 'Liquidacion de deuda por deposito')], string='Estado',
        default='draft', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Moneda', related='loan_calculator_ids.currency_id')
    currency_id_dollar = fields.Many2one('res.currency', string='Moneda en Dólares',
                                         default=lambda self: self.env.ref('base.USD'))
    @api.onchange('amount_total')
    def _change_amount_total_bs(self):
        for rec in self:
            rec.amount_total_bs = rec.amount_total * rec.currency_id_dollar.inverse_rate

    @api.depends('date')
    def _compute_period(self):
        for rec in self:
            rec.period = rec.date.strftime('%m/%Y')

    # @api.depends('mount')
    # def _compute_interest(self):
    #     for rec in self:
    #         rec.interest = rec.mount * 0.1

    @api.depends('capital_initial', 'balance_capital', 'interest', 'res_social')
    def _compute_interest(self):
        percentage_interest = float(
            self.env['ir.config_parameter'].sudo().get_param('rod_cooperativa.monthly_interest'))
        contingency_found = float(self.env['ir.config_parameter'].sudo().get_param('rod_cooperativa.contingency_fund'))

        interest = (percentage_interest + contingency_found) / 100

        mortgage_loan = float(self.env['ir.config_parameter'].sudo().get_param('rod_cooperativa.mortgage_loan'))
        percentage_interest_mortgage = float(
            self.env['ir.config_parameter'].sudo().get_param('rod_cooperativa.monthly_interest_mortgage'))

        interest_mortgage = (percentage_interest_mortgage + mortgage_loan) / 100

        for rec in self:
            if rec.loan_calculator_ids.with_guarantor == 'loan_guarantor' or rec.loan_calculator_ids.with_guarantor == 'no_loan_guarantor':
                rec.interest = rec.capital_initial * interest
                rec.interest_base = rec.capital_initial * round((percentage_interest / 100), 3)
                rec.capital_index_initial = round(rec.mount - rec.interest, 2)
            if rec.loan_calculator_ids.with_guarantor == 'mortgage':
                rec.interest_mortgage = rec.capital_initial * interest_mortgage
                rec.interest_base_mortgage = rec.capital_initial * (percentage_interest_mortgage / 100)
                rec.capital_index_initial = round(rec.mount - rec.interest_mortgage, 2)
            rec.balance_capital = rec.capital_initial - rec.capital_index_initial
            if rec.loan_calculator_ids.with_guarantor == 'loan_guarantor' or rec.loan_calculator_ids.with_guarantor == 'no_loan_guarantor':
                rec.res_social = rec.capital_initial * round((contingency_found / 100), 4)
            if rec.loan_calculator_ids.with_guarantor == 'mortgage':
                rec.res_mortgage = rec.capital_initial * round((mortgage_loan / 100), 4)
            rec.amount_total = round(rec.mount, 2) + round(rec.percentage_amount_min_def, 2) + round(
                rec.interest_month_surpluy, 2)
            rec._change_amount_total_bs()
            # rec.commission_min_def = round((commission_min_def / 100) * rec.amount_total_bs,2)
            # commision_auxiliar = rec.commission_min_def
            # rec.amount_returned_coa = round(rec.amount_total_bs,2) - commision_auxiliar
    def open_loan_payment(self, context=None):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Model Title',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self.id,
            'target': 'current',
        }

    def confirm_payment(self):
        for record in self:
            if record.state == 'draft':
                record.write({'state': 'transfer'})

    def confirm_ministry_defense(self):
        for record in self:
            if record.state == 'draft':
                record.write({'state': 'ministry_defense'})

    def draft_massive(self):
        for record in self:
            record.write({'state': 'draft'})

    def debt_settlement_min_def(self):
        for record in self:
            if record.state == 'draft':
                record.write({'state': 'debt_settlement_mindef'})

    def debt_settlement_deposit(self):
        for record in self:
            if record.state == 'draft':
                record.write({'state': 'debt_settlement_deposit'})
