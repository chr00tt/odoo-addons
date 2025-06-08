# -*- coding: utf-8 -*-

{
    'name': '国家医疗保障局 - 医保疾病诊断、手术操作分类与代码数据',
    'author': 'He Jian',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'category': 'Inventory/Inventory',
    'depends': [
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'data/nhsa.jbzd.csv', # 采用异步导入
        'views/nhsa_jbzd_views.xml',
    ],
    'post_init_hook': '_import_nhsa_jbzd',
    'license': 'LGPL-3',
}
