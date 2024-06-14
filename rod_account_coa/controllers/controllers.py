# -*- coding: utf-8 -*-
# from odoo import http


# class RodAccountCoa(http.Controller):
#     @http.route('/rod_account_coa/rod_account_coa', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_account_coa/rod_account_coa/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_account_coa.listing', {
#             'root': '/rod_account_coa/rod_account_coa',
#             'objects': http.request.env['rod_account_coa.rod_account_coa'].search([]),
#         })

#     @http.route('/rod_account_coa/rod_account_coa/objects/<model("rod_account_coa.rod_account_coa"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_account_coa.object', {
#             'object': obj
#         })
