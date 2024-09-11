# -*- coding: utf-8 -*-
# from odoo import http


# class RodDynamicReport(http.Controller):
#     @http.route('/rod_dynamic_report/rod_dynamic_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rod_dynamic_report/rod_dynamic_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rod_dynamic_report.listing', {
#             'root': '/rod_dynamic_report/rod_dynamic_report',
#             'objects': http.request.env['rod_dynamic_report.rod_dynamic_report'].search([]),
#         })

#     @http.route('/rod_dynamic_report/rod_dynamic_report/objects/<model("rod_dynamic_report.rod_dynamic_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rod_dynamic_report.object', {
#             'object': obj
#         })
