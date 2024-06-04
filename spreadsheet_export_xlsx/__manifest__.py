# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Spreadsheet export xlsx",
    'author': "He Jian",
    'category': 'Hidden',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': ['spreadsheet_oca'],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
    'assets': {
        'spreadsheet.o_spreadsheet': [
            'spreadsheet_export_xlsx/static/src/bundle/spreadsheet_renderer.esm.js',
            'spreadsheet_export_xlsx/static/src/menu_item_registry.js',
        ],
    }
}
