# -*- coding: utf-8 -*-


{
    'name': "CRM enterprise extension",
    'version': "1.0",
    'category': "Sales/CRM Extension",
    'description': """
    """,
    'depends': ['crm', 'sale' ],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/crm_lead_service_views.xml'
    ],
    'installable': True,
    'auto_install': ['crm'],
    'license': 'LGPL-3',
}
