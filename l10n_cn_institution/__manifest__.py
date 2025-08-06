# -*- coding: utf-8 -*-

{
    'name': '中国 - 行政事业单位会计',
    'icon': '/account/static/description/l10n.png',
    'countries': ['cn'],
    'category': 'Accounting/Localizations/Account Charts',
    'author': "He Jian",
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': [
        'account',
        'l10n_cn',

        'l10n_cn_institution_budget',
    ],
    'data': [
        'data/account.account.tag.csv',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
