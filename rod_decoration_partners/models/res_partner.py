from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    decoration_ids = fields.One2many('decoration.partners', 'partner_id', string='Condecoraciones')
