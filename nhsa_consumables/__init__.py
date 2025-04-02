# -*- coding: utf-8 -*-

from . import models

# from odoo.addons.base_import.models.base_import import Import
# from odoo.modules import get_module_path

# def _import_nhsa_consumables(env):
#     file_path = get_module_path('nhsa_consumables') + '/data/nhsa.consumables.csv'
#     with open(file_path, 'r', encoding='utf-8') as file:
#         file_content = file.read()

#         import_obj = Import(env)
#         import_obj.res_model = 'nhsa.consumables'
#         import_obj.file = file_content
#         import_obj.file_name = 'nhsa.consumables.csv'
#         import_obj.do(header=True, encoding='utf-8', separator=',', quoting='"', use_queue=True, chunk_size=100)
