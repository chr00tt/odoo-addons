# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '医用耗材 - 采购',
    'author': 'He Jian',
    'category': 'Inventory/Purchase',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': [
        'purchase',
        'medical_consumables_product',
    ],
    'data': [
        'views/purchase_views.xml',
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
