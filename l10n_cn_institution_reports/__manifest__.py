# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '中国 - 行政事业单位会计 - 会计报表',
    'category': 'Accounting/Localizations',
    'depends': ['l10n_cn_institution', 'account_reports'],
    'data': [
        'data/menuitems.xml',
        'data/balance_sheet.xml',
        'data/income_and_expense.xml',
        'data/budget_income_and_expense.xml',
        'data/account_financial_report_data.xml',
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}