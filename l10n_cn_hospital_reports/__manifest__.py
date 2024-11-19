# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '中国 - 医院会计 - 会计报表',
    'category': 'Accounting/Localizations',
    'depends': ['l10n_cn_hospital', 'l10n_cn_institution_reports'],
    'data': [
        'data/balance_sheet.xml',
        'data/budget_income_and_expense.xml',
        'data/income_and_expense.xml',
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
