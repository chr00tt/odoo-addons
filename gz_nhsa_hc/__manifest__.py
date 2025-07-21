# -*- coding: utf-8 -*-

{
    'name': '贵州省医疗保障局 - 耗材数据',
    'author': 'He Jian',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'category': 'Inventory/Inventory',
    'depends': [
        'stock',

        'nhsa_hc',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/gz.medical.consumables.csv',
        'views/gz_medical_consumables_views.xml',
        'views/product_views.xml',
        'views/stock_menu_views.xml',
    ],
    'license': 'LGPL-3',
}
