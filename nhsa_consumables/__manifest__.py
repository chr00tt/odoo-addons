# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '国家医疗保障局 - 耗材数据',
    'author': 'He Jian',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'category': 'Inventory/Inventory',
    'depends': [
        'stock',

        'medical_consumables_product',
        ],
    'data': [
        'security/ir.model.access.csv',
        'data/nhsa_consumables_data.xml',
        'data/nhsa.consumables.category.csv',
        'data/nhsa.consumables.csv',
        'views/nhsa_consumables_views.xml',
        'views/nhsa_consumables_category_views.xml',
        'views/product_views.xml',
        'views/stock_menu_views.xml',
        'views/product_supplierinfo_views.xml',
    ],
    'license': 'LGPL-3',
}
