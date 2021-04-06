# -*- coding: utf-8 -*-
{
    'name': "totem_proyect",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','base_setup','website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/MainView.xml',
        'views/EventView.xml',
        'views/SliderView.xml',
        'views/UsersView.xml',
        'views/ScreenView.xml',
        'views/web_assets_backend.xml',
        'views/ResConfigView.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'qweb': [
        'static/src/xml/ClientView.xml',  
    ],
    'application': True,
}