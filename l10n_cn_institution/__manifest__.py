# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '中国 - 行政事业单位会计',
    'icon': '/account/static/description/l10n.png',
    'countries': ['cn'],
    'category': 'Accounting/Localizations/Account Charts',
    'author': "He Jian",
    'website': 'https://github.com/chr00tt/odoo-addons',
    'description': """
行政事业单位会计制度、医院会计制度。
    """,
    'depends': ['l10n_cn'],
    'data': [
        'data/account.account.tag.csv',
        'data/product.category.csv',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
