# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '高德地图地理位置',
    'author': "He Jian",
    'category': 'Hidden/Tools',
    'description': """
高德地图地理位置
========================
    """,
    'depends': ['base_geolocalize'],
    'data': [
        'views/res_config_settings_views.xml',
        'data/data.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
