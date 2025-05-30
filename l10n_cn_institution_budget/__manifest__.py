# -*- coding: utf-8 -*-

{
    'name': '中国 - 行政事业单位会计 - 预算会计',
    'icon': '/account/static/description/l10n.png',
    'countries': ['cn'],
    'author': "He Jian",
    'category': 'Accounting/Localizations',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': ['l10n_cn'],
    'data': [
        'views/account_account_views.xml',
        'views/account_move_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'l10n_cn_institution_budget/static/src/components/**/*',
        ],
    },
    'license': 'LGPL-3',
}
