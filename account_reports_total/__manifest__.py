# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : '会计报表 - 合计',
    'author': "He Jian",
    'summary': '提供本日合计、本月合计、本年累计。',
    'category': 'Accounting/Accounting',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': ['account_reports'],
    'data': [
        'data/general_ledger.xml',
        'views/account_report_view.xml',
        'views/report_templates.xml',
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
