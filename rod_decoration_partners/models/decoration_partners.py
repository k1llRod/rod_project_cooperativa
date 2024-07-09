from odoo import models, fields, api

class DecorationPartners(models.Model):
    _name = 'decoration.partners'
    _description = 'Decoration Partners'

    name = fields.Char(string='Condecoracion')
    description = fields.Text(string='Description', required=True)
    date = fields.Date(string='Fecha', required=True)
    partner_id = fields.Many2one('res.partner', string='Socio')
    type_decoration = fields.Selection([('first','Primera'),
                                        ('second','Segunda'),
                                        ('third','Tercera'),
                                        ('only','Unica')], string='Tipo de Condecoracion', required=True)
    resolution_ids = fields.Many2one('resolution', string='Resolucion', required=True)

    @api.model
    def create(self, vals):
        name = self.env['ir.sequence'].next_by_code('decoration.partners')
        vals['name'] = name
        res = super(DecorationPartners, self).create(vals)
        return res