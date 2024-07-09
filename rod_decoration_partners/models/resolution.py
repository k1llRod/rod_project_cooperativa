from odoo import models, fields, api, _

class Resolution(models.Model):
    _name = 'resolution'
    _description = 'Resolutions'

    name = fields.Char(string='Resolucion')
    description = fields.Text(string='Description')
    date = fields.Date(string='Fecha')
