# -*- coding: utf-8 -*-
{
    'name': "rod_loan_emergency",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','mail','rod_cooperativa'],

    # always loaded
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/loan_application_emergency.xml',
        'views/loan_payment_emergency.xml',
        'views/rod_loan_emergency_menuitem.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
