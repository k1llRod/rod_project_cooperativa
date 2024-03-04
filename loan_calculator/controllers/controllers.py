# -*- coding: utf-8 -*-
# from odoo import http


# class LoanCalculator(http.Controller):
#     @http.route('/loan_calculator/loan_calculator', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/loan_calculator/loan_calculator/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('loan_calculator.listing', {
#             'root': '/loan_calculator/loan_calculator',
#             'objects': http.request.env['loan_calculator.loan_calculator'].search([]),
#         })

#     @http.route('/loan_calculator/loan_calculator/objects/<model("loan_calculator.loan_calculator"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('loan_calculator.object', {
#             'object': obj
#         })
