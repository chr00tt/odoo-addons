# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Web hide zero monetary',
    'website': 'https://github.com/chr00tt/web_hide_zero_monetary',
    'author': "He Jian",
    'category': 'Hidden',
    'description':
        """
不显示其值为 0 的金额。
        """,
    'depends': ['web'],
    'auto_install': True,
    'data': [
        'views/webclient_templates.xml',
    ],
    'license': 'LGPL-3',
}
