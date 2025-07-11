# -*- coding: utf-8 -*-

{
    'name': '医用耗材 - 库存',
    'author': 'He Jian',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': [
        'stock',
        'medical_consumables_product',
    ],
    'category': 'Inventory/Inventory',
    'data': [
        'views/stock_move_line_views.xml',
        'views/stock_move_views.xml',
        'views/stock_picking_views.xml',
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
