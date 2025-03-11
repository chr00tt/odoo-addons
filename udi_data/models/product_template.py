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

    @api.onchange('ybbm')
    def _ybbm_to_udi_data(self):
        if self.ybbm:
            udi_data = self.env['udi.data'].search([('ybbm', '=', self.ybbm)], limit=1)
            if udi_data:
                self.udi_data_id = udi_data.id

    @api.onchange('udi_data_id')
    def _onchange_udi_data_id(self):
        if self.udi_data_id:
            # 如果有医保耗材分类编码，并且未设置医保医用耗材分类与代码
            if self.udi_data_id.ybbm and not self.nhsa_consumables_id:
                self.nhsa_consumables_id = self.udi_data_id.nhsa_consumables_id

            # 如果有最小销售单元产品标识，并且未设置条码
            if self.udi_data_id.zxxsdycpbs and not self.barcode:
                self.barcode = self.udi_data_id.zxxsdycpbs
