# -*- coding: utf-8 -*-
# from odoo import http


# class RodConsumerLoan(http.Controller):
#     @http.route('/rod_consumer_loan/rod_consumer_loan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_consumer_loan/rod_consumer_loan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_consumer_loan.listing', {
#             'root': '/rod_consumer_loan/rod_consumer_loan',
#             'objects': http.request.env['rod_consumer_loan.rod_consumer_loan'].search([]),
#         })

#     @http.route('/rod_consumer_loan/rod_consumer_loan/objects/<model("rod_consumer_loan.rod_consumer_loan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_consumer_loan.object', {
#             'object': obj
#         })
