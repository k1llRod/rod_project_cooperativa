from odoo import models, fields, api

class DecorationPartners(models.Model):
    _name = 'decoration.partners'
    _description = 'Decoration Partners'

    _columns = {
        'archive_decoration': fields.Binary('Archivo de Condecoracion'),
        'file_name': fields.Char('Nombre de Archivo'),
    }

    name = fields.Char(string='Condecoracion')
    name_partner_decoration = fields.Char(string='Nombre completo', required=True)
    description = fields.Text(string='Descripcion', required=True)
    date = fields.Date(string='Fecha', required=True)
    partner_id = fields.Many2one('res.partner', string='Socio')
    type_decoration = fields.Selection([('first','Primera'),
                                        ('second','Segunda'),
                                        ('third','Tercera'),
                                        ('only','Unica')], string='Tipo de Condecoracion', required=True)
    archive_decoration = fields.Binary(string='Archivo de Condecoracion')
    file_name = fields.Char('Nombre de Archivo')
    resolution_ids = fields.Many2one('resolution', string='Resolucion', required=True)
    auxiliar_partner_ids = fields.Many2one('auxiliar.partners', string='Socio Auxiliar')
    @api.model
    def create(self, vals):
        name = self.env['ir.sequence'].next_by_code('decoration.partners')
        vals['name'] = name
        res = super(DecorationPartners, self).create(vals)
        return res