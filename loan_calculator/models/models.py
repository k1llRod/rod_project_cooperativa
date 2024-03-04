# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class loan_calculator(models.Model):
#     _name = 'loan_calculator.loan_calculator'
#     _description = 'loan_calculator.loan_calculator'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
