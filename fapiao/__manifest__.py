# -*- coding: utf-8 -*-
{
    'name' : '发票',
    'author': 'He Jian',
    'description': '管理账单的发票，以满足医保接口需要。',
    'category': 'Accounting/Accounting',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_views.xml',
        'views/fapiao_views.xml',
    ],
    'license': 'LGPL-3',
}
