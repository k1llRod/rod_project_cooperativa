# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class rod_account_coa(models.Model):
#     _name = 'rod_account_coa.rod_account_coa'
#     _description = 'rod_account_coa.rod_account_coa'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
