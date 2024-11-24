# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '中国 - 行政事业单位会计 - 会计报表',
    'category': 'Accounting/Localizations',
    'depends': ['l10n_cn_institution', 'account_reports'],
    'data': [
        'data/balance_sheet.xml',
        'data/income_and_expense.xml',
        'data/budget_income_and_expense.xml',
        'data/institution_report_actions.xml',
        'data/menuitems.xml',
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
