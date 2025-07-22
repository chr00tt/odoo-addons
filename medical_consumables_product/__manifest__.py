# -*- coding: utf-8 -*-

{
    'name': '医用耗材 - 产品和价格表',
    'author': 'He Jian',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'category': 'Inventory/Inventory',
    'depends': [
        'product',

        'product_manufacturer',
    ],
    'data': [
        'views/product_supplierinfo_views.xml',
        'views/product_template_views.xml',
        'views/product_views.xml',
    ],
    'license': 'LGPL-3',
}
