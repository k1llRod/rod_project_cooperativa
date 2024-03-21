# -*- coding: utf-8 -*-
# from odoo import http


# class RodLoanEmergency(http.Controller):
#     @http.route('/rod_loan_emergency/rod_loan_emergency', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_loan_emergency/rod_loan_emergency/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_loan_emergency.listing', {
#             'root': '/rod_loan_emergency/rod_loan_emergency',
#             'objects': http.request.env['rod_loan_emergency.rod_loan_emergency'].search([]),
#         })

#     @http.route('/rod_loan_emergency/rod_loan_emergency/objects/<model("rod_loan_emergency.rod_loan_emergency"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_loan_emergency.object', {
#             'object': obj
#         })
