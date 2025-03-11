# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _, SUPERUSER_ID

class ProductTemplate(models.Model):
    _inherit = "product.template"

    udi_data_id = fields.Many2one('udi.data', '医疗器械唯一标识')

    udi_zxxsdycpbs = fields.Char("最小销售单元产品标识")
    udi_sydycpbs = fields.Boolean("使用单元产品标识")
    udi_btcpbs = fields.Boolean("本体产品标识")
    udi_cpmctymc = fields.Char("产品名称/通用名称")
    udi_spmc = fields.Char("商品名称")
    udi_ggxh = fields.Char("型号规格/包装规格")
