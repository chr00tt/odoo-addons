# -*- coding: utf-8 -*-

{
    'name': '中国 - 企业会计',
    'author': "He Jian",
    'category': 'Accounting/Localizations/Account Charts',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': ['l10n_cn_base'],
    'data': [
        'data/account_data.xml',
        'data/l10n_cn_enterprise_coa_chart_data.xml',
        'data/account.account.template.csv',
        'data/l10n_cn_enterprise_coa_chart_post_data.xml',
        'data/account_tax_template_data.xml',
        'data/account_chart_template_data.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
        'demo/l10n_cn_enterprise_demo.xml',
        'demo/account.account.csv',
        'demo/res.bank.csv',
        'demo/res.partner.bank.csv',
        'demo/account.journal.csv',
        'demo/account.move.csv',
    ],
    'license': 'LGPL-3',
}
