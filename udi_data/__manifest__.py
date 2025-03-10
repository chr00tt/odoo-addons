# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '医疗器械唯一标识数据库',
    'author': 'He Jian',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': ['stock'],
    'category': 'Inventory/Inventory',
    'data': [
        'security/ir.model.access.csv',
        'views/udi_data_views.xml',
        'views/stock_menu_views.xml',
    ],
    'license': 'LGPL-3',
}
