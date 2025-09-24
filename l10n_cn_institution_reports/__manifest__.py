# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '中国 - 行政事业单位会计 - 会计报表',
    'author': 'He Jian',
    'category': 'Accounting/Localizations',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': ['l10n_cn_institution', 'account_reports'],
    'data': [
        'data/balance_sheet.xml',
        'data/cash_flow_report.xml',
        'data/income_and_expense.xml',
        'data/budget_income_and_expense.xml',
        'data/institution_report_actions.xml',
        'data/menuitems.xml',
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
