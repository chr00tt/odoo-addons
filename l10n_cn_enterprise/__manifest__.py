# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '中国 - 企业会计',
    'author': "He Jian",
    'category': 'Accounting/Localizations/Account Charts',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': ['l10n_cn'],
    'data': [
        'data/l10n_cn_enterprise_coa.xml',
        'data/account.group.template.csv',
        'data/account.account.tag.csv',
        'data/account.account.template.csv',
        'data/l10n_cn_enterprise_coa_post.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
        'demo/cn_account_demo.xml',
        'demo/account.account.csv',
        'demo/account.group.csv',
        'demo/analytic_account_demo.xml',
        'demo/res.bank.csv',
        'demo/res.partner.bank.csv',
        'demo/account.journal.csv',
        'demo/account.move.csv',
    ],
    'license': 'LGPL-3',
}
