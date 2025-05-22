# -*- coding: utf-8 -*-

from . import models

def _import_nhsa_consumables(env):
    from odoo.modules import get_module_path

    # 导入生产厂家
    file_path = get_module_path('nhsa_consumables') + '/data/res.partner.csv'
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

        import_obj = env['base_import.import'].create({
            'res_model': 'res.partner',
            'file': file_content,
            'file_name': 'res.partner.csv',
            'file_type': 'text/csv',
        })
        import_obj.execute_import(
            ['id', 'name', 'ref', 'company_type', 'category_id/id'],
            ['id', 'name', 'ref', 'company_type', 'category_id/id'],
            {
                'has_headers': True, 'encoding': 'utf-8', 'separator': ',', 'quoting': '"',
                'use_queue': True, 'chunk_size': 1000, 'priority': 100,
                'context': {
                    'res_partner_search_mode': 'manufacturer',
                },
            }
        )

    # 导入耗材代码
    file_path = get_module_path('nhsa_consumables') + '/data/nhsa.consumables.csv'
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

        import_obj = env['base_import.import'].create({
            'res_model': 'nhsa.consumables',
            'file': file_content,
            'file_name': 'nhsa.consumables.csv',
            'file_type': 'text/csv',
        })
        import_obj.execute_import(
            ['id', 'name', 'nhsa_consumables_categ_id/id','common_name','material','specifications','enterprise'],
            ['id', 'name', 'nhsa_consumables_categ_id/id','common_name','material','specifications','enterprise'],
            {
                'has_headers': True, 'encoding': 'utf-8', 'separator': ',', 'quoting': '"',
                'use_queue': True, 'chunk_size': 10000, 'priority': 200,
            }
        )
