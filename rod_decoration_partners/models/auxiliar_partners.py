from odoo import models, fields, api

class AuxiliarPartners(models.Model):
    _name = 'auxiliar.partners'
    _description = 'Auxiliar Partners'

    name = fields.Char(string='Nombre completo', required=True)
    grade = fields.Char(string='Grado')
    date = fields.Date(string='Fecha de registro')
    partner_id = fields.Many2one('res.partner', string='Socio')
    decoration_ids = fields.One2many('decoration.partners', 'auxiliar_partner_ids', string='Condecoraciones')
