# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : '现金流量表',
    'author': "He Jian",
    'summary': '允许用户修改凭证分录的现金流量分配。',
    'category': 'Accounting/Accounting',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': ['account_reports'],
    'data': [
        'views/account_move_views.xml',
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
