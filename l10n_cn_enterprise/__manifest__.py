# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '中国 - 企业会计',
    'author': "He Jian",
    'category': 'Accounting/Localizations/Account Charts',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': ['l10n_cn_base'],
    'data': [
        'data/l10n_cn_enterprise_coa.xml',
        'data/account.account.template.csv',
        'data/l10n_cn_enterprise_coa_post.xml',
        'data/account_chart_template_data.yml',
    ],
    'license': 'LGPL-3',
}