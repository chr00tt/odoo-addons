# -*- coding: utf-8 -*-

from . import models

def _import_nhsa_icd10(env):
    from odoo.modules import get_module_path

    # 导入分类
    file_path = get_module_path('nhsa_icd10') + '/data/icd10.category.csv'
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

        import_obj = env['base_import.import'].create({
            'res_model': 'icd10.category',
            'file': file_content,
            'file_name': 'icd10.category.csv',
            'file_type': 'text/csv',
        })
        import_obj.execute_import(
            ['id', 'name', 'code', 'parent_id/id'],
            ['id', 'name', 'code', 'parent_id/id'],
            {
                'has_headers': True, 'encoding': 'utf-8', 'separator': ',', 'quoting': '"',
                'use_queue': True, 'chunk_size': 1000, 'priority': 100,
            }
        )

    # 导入诊断代码
    file_path = get_module_path('nhsa_icd10') + '/data/icd10.code.csv'
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

        import_obj = env['base_import.import'].create({
            'res_model': 'icd10.code',
            'file': file_content,
            'file_name': 'icd10.code.csv',
            'file_type': 'text/csv',
        })
        import_obj.execute_import(
            ['id', 'code', 'name','category_id/id'],
            ['id', 'code', 'name','category_id/id'],
            {
                'has_headers': True, 'encoding': 'utf-8', 'separator': ',', 'quoting': '"',
                'use_queue': True, 'chunk_size': 1000, 'priority': 200,
            }
        )
