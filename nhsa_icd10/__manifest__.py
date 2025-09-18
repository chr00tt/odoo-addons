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
        'data/nhsa_icd10_data.xml',
        'views/icd10_code_views.xml',
        # 'data/icd10.category.csv', # 通过代码导入
    ],
    'post_init_hook': '_import_nhsa_icd10',
    'license': 'LGPL-3',
}
