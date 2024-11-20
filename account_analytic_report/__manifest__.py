# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : '会计 - 分析项目报表',
    'author': "He Jian",
    'category': 'Accounting/Accounting',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': ['account_reports'],
    'data': [
        'data/analytic_report.xml',
        'data/account_report_actions.xml',
        'data/menuitems.xml',
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
