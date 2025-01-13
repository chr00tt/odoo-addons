# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Web hide zero monetary',
    'author': "He Jian",
    'category': 'Hidden',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'description':
        """
不显示 0.00 。
        """,
    'depends': ['web'],
    'data': [
        'views/webclient_templates.xml',
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
