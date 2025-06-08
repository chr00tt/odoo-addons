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
        'data/res_partner_category_data.xml',
        'data/nhsa_consumables_data.xml',
        'data/nhsa.consumables.category.csv',
        # 'data/res.partner.csv', # 采用异步导入
        # 'data/nhsa.consumables.csv', # 采用异步导入
        'views/nhsa_consumables_views.xml',
        'views/nhsa_consumables_category_views.xml',
        'views/product_views.xml',
        'views/res_partner_views.xml',
        'views/stock_menu_views.xml',
        'views/product_supplierinfo_views.xml',
    ],
    'post_init_hook': '_import_nhsa_hc',
    'license': 'LGPL-3',
}
