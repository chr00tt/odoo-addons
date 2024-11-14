# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '中国 - 医院会计',
    'icon': '/account/static/description/l10n.png',
    'countries': ['cn'],
    'category': 'Accounting/Localizations/Account Charts',
    'author': "He Jian",
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': ['l10n_cn_institution'],
    'data': [
        'data/l10n_cn_hospital_coa.xml',
        'data/account.group.template.csv',
        'data/account.account.template.csv',
        'data/l10n_cn_hospital_coa_post.xml',
        'data/product.category.csv',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
