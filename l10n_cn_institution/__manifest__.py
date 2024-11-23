# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '中国 - 行政事业单位会计',
    'author': "He Jian",
    'category': 'Accounting/Localizations/Account Charts',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': ['l10n_cn_base'],
    'data': [
        'data/l10n_cn_institution_coa.xml',
        'data/account.group.csv',
        'data/account.account.template.csv',
        'data/l10n_cn_institution_coa_post.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
