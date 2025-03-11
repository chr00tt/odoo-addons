# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _, SUPERUSER_ID

class ProductTemplate(models.Model):
    _inherit = "product.template"

    udi_data_id = fields.Many2one('udi.data', '医疗器械唯一标识')

    udi_zxxsdycpbs = fields.Char(related='udi_data_id.zxxsdycpbs')
    udi_sydycpbs = fields.Char(related='udi_data_id.sydycpbs')
    udi_btcpbs = fields.Char(related='udi_data_id.btcpbs')
    udi_cpmctymc = fields.Char(related='udi_data_id.cpmctymc')
    udi_spmc = fields.Char(related='udi_data_id.spmc')
    udi_ggxh = fields.Char(related='udi_data_id.ggxh')
