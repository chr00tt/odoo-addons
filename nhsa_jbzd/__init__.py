# -*- coding: utf-8 -*-

from . import models

def _import_nhsa_jbzd(env):
    from odoo.modules import get_module_path

    file_path = get_module_path('nhsa_jbzd') + '/data/nhsa.jbzd.csv'
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

        import_obj = env['base_import.import'].create({
            'res_model': 'nhsa.jbzd',
            'file': file_content,
            'file_name': 'nhsa.jbzd.csv',
            'file_type': 'text/csv',
        })
        import_obj.execute_import(
            ['id', 'code', 'master_code', 'name', 'category'],
            ['id', 'code', 'master_code', 'name', 'category'],
            {
                'has_headers': True, 'encoding': 'utf-8', 'separator': ',', 'quoting': '"',
                'use_queue': True, 'chunk_size': 1000, 'priority': 0,
            }
        )
