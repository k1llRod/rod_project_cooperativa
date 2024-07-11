from odoo import models, fields, api, _

class Resolution(models.Model):
    _name = 'resolution'
    _description = 'Resolutions'
    _columns = {
        'archive_decoration': fields.Binary('Archivo de Condecoracion'),
        'file_name': fields.Char('Nombre de Archivo'),
    }
    name = fields.Char(string='Resolucion')
    description = fields.Text(string='Descripcion')
    date = fields.Date(string='Fecha')
    archive_decoration = fields.Binary(string='Archivo de resolucion' )
    file_name = fields.Char('Nombre de Archivo')