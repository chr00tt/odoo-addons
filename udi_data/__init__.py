# -*- coding: utf-8 -*-

from . import models

def _udi_data_import_data(env):
    from odoo.modules import get_module_path

    # 导入医疗器械分类
    file_path = get_module_path('udi_data') + '/data/medical.device.category.csv'
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

        import_obj = env['base_import.import'].create({
            'res_model': 'medical.device.category',
            'file': file_content,
            'file_name': 'medical.device.category.csv',
            'file_type': 'text/csv',
        })
        import_obj.execute_import(
            ['id', 'name', 'code', 'parent_id/id', 'cpms', 'yqyt', 'pmjl', 'gllb'],
            ['id', 'name', 'code', 'parent_id/id', 'cpms', 'yqyt', 'pmjl', 'gllb'],
            {
                'has_headers': True, 'encoding': 'utf-8', 'separator': ',', 'quoting': '"',
                'use_queue': True, 'chunk_size': 400, 'priority': 100,
            }
        )
