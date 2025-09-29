# -*- coding: utf-8 -*-

{
    'name': "Barcode Production Date",
    'author': 'He Jian',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'category': 'Inventory/Inventory',
    'depends': [
        'stock_barcode',

        'stock_lot_production_date',
    ],
    'data': [
        'views/stock_move_line_views.xml',
    ],
    'auto_install': True,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'stock_barcode_production_date/static/src/**/*',
        ],
    },
}
