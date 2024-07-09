# -*- coding: utf-8 -*-
# from odoo import http


# class RodDecorationPartners(http.Controller):
#     @http.route('/rod_decoration_partners/rod_decoration_partners', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_decoration_partners/rod_decoration_partners/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_decoration_partners.listing', {
#             'root': '/rod_decoration_partners/rod_decoration_partners',
#             'objects': http.request.env['rod_decoration_partners.rod_decoration_partners'].search([]),
#         })

#     @http.route('/rod_decoration_partners/rod_decoration_partners/objects/<model("rod_decoration_partners.rod_decoration_partners"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_decoration_partners.object', {
#             'object': obj
#         })
