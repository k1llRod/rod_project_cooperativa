# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rod_service_loan(models.Model):
#     _name = 'rod_service_loan.rod_service_loan'
#     _description = 'rod_service_loan.rod_service_loan'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
