# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Web hide zero monetary',
    'author': "He Jian",
    'category': 'Hidden',
    'depends': ['web'],
    'auto_install': True,
    'assets': {
        'web.assets_backend': [
            'web_hide_zero_monetary/static/src/legacy/js/fields/*',
        ],
    },
    'license': 'LGPL-3',
}
