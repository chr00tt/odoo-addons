# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '医疗器械唯一标识数据库',
    'author': 'He Jian',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': [
        'stock',

        'product_manufacturer',

        'medical_consumables_product',
        'nhsa_consumables',
        ],
    'category': 'Inventory/Inventory',
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'data/udi_data_data.xml',
        'data/medical.device.category.csv',
        'views/product_views.xml',
        'views/udi_data_views.xml',
        'views/medical_device_category_views.xml',
        'views/stock_menu_views.xml',
        'views/nhsa_consumables_category_views.xml',
        'views/nhsa_consumables_views.xml',
    ],
    'license': 'LGPL-3',
}
