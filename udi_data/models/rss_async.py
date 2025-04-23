# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

import os

class RssMixin(models.AbstractModel):
    _inherit = 'rss.mixin'

    # 异步导入数据文件
    def _import_data_files(self, directory):
        for root, _, files in os.walk(directory):
            for file in files:
                description = '从 %s 导入唯一标识' % file
                if file.endswith('.xml'):
                    self.with_delay(description=description, priority=1000)._import_xml(os.path.join(root, file))
                elif file.endswith('.zip'):
                    extract_dir = self._extract_zip(directory + '/' + file)
                    self.with_delay(description=description, priority=1000)._import_data_files(extract_dir)
