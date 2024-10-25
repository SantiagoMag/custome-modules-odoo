# -*- coding: utf-8 -*-


{
    'name': "Credit Risk Module",
    'version': "1.1",
    'category': "Credit Risk Module",
    'description': """
    """,
    'depends': [ 'base' ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/credit_risk_view.xml',
        'views/res_config_settings_views.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
