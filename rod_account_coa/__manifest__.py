# -*- coding: utf-8 -*-
{
    'name': "rod_account_coa",

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
    'depends': ['base','account','rod_cooperativa','mail','rod_cooperativa_aportes', 'contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/rod_account_coa_menuitem.xml',
        'views/account_payment_coa.xml',
        'views/account_move.xml',
        'views/account_payment.xml',
        'wizard/wizard_payroll.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
}
