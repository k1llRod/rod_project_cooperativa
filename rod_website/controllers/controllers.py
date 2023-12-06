# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class RodWebsite(http.Controller):
    @http.route('/rod_website/rod_website', auth='public', website=True)
    def index(self, **kw):
        return request.render('rod_website.index')

    @http.route('/rod_website/rod_website/objects', auth='public', website=True)
    def list(self, **kw):
        return http.request.render('rod_website.listing', {
            'root': '/rod_website/rod_website',
            'objects': http.request.env['rod_website.rod_website'].search([]),
        })

    @http.route('/rod_website/rod_website/objects/<model("rod_website.rod_website"):obj>', auth='public', website=True)
    def object(self, obj, **kw):
        return http.request.render('rod_website.object', {
            'object': obj
        })


# class RodWebsite(http.Controller):
#     @http.route('/rod_website/rod_website', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_website/rod_website/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_website.listing', {
#             'root': '/rod_website/rod_website',
#             'objects': http.request.env['rod_website.rod_website'].search([]),
#         })

#     @http.route('/rod_website/rod_website/objects/<model("rod_website.rod_website"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_website.object', {
#             'object': obj
#         })
