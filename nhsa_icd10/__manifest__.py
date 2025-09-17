# -*- coding: utf-8 -*-

{
    'name': 'ICD-10 诊断代码',
    'author': 'He Jian',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': [
        'base',
        'web',
    ],
    'category': 'Inventory/Inventory',
    'data': [
        'security/ir.model.access.csv',
        'views/icd10_code_views.xml',
        'data/icd10.category.csv',
    ],
    'license': 'LGPL-3',
}
