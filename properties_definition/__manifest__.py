# -*- coding: utf-8 -*-

{
    'name': 'Properties definition',
    'version': '1.10',
    'category': 'Hidden',
    'sequence': 145,
    'description': """
Properties definition for Odoo field.
=====================================
Enter the definition if field ttype is properties on field edit view.
    """,
    'website': 'https://github.com/chr00tt/properties_definition',
    'depends': ['base'],
    'data': [
        'views/ir_model_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3',
}
