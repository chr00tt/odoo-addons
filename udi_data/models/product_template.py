# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    udi_data_id = fields.Many2one('udi.data', '医疗器械唯一标识', compute='_compute_udi_data_id', store=True)

    syqsfxyjxmj = fields.Boolean("使用前是否需要进行灭菌")
    gllb = fields.Selection([('1', 'Ⅰ'), ('2', 'Ⅱ'), ('3', 'Ⅲ')], string='管理类别', default='1')

    udi_flbm = fields.Many2one('medical.device.category', related='udi_data_id.flbm', store=True)

    udi_zxxsdycpbs = fields.Char(related='udi_data_id.zxxsdycpbs')
    udi_sydycpbs = fields.Char(related='udi_data_id.sydycpbs')
    udi_btcpbs = fields.Char(related='udi_data_id.btcpbs')
    udi_cpmctymc = fields.Char(related='udi_data_id.cpmctymc')
    udi_spmc = fields.Char(related='udi_data_id.spmc')
    udi_ggxh = fields.Char(related='udi_data_id.ggxh')

    @api.depends('ybbm')
    def _compute_udi_data_id(self):
        for template in self:
            if template.ybbm:
                udi_data = self.env['udi.data'].search([('ybbm', '=', template.ybbm)], limit=1)
                if udi_data:
                    template.udi_data_id = udi_data.id

    @api.onchange('udi_data_id')
    def _onchange_udi_data_id(self):
        if self.udi_data_id:
            # 设置医用耗材标志
            self.is_medical_consumables = self.udi_data_id.cplb == '耗材'

            # 设置医保医用耗材分类与代码
            if self.udi_data_id.ybbm and not self.nhsa_consumables_id:
                self.nhsa_consumables_id = self.udi_data_id.nhsa_consumables_id

            # 设置条码
            if not self.barcode:
                self.barcode = self.udi_data_id.sydycpbs if self.udi_data_id.sydycpbs else self.udi_data_id.zxxsdycpbs

            # 设置规格
            if not self.ggxh and self.udi_data_id.ggxh:
                self.ggxh = self.udi_data_id.ggxh

            # 设置追溯
            if self.udi_data_id.scbssfbhxlh:
                self.tracking = 'serial'
            elif self.udi_data_id.scbssfbhph and self.tracking != 'serial':
                self.tracking = 'lot'
            if self.udi_data_id.scbssfbhsxrq:
                self.use_expiration_date = True

            # 设置内部说明
            if not self.description and self.udi_data_id.cpms:
                self.description = self.udi_data_id.cpms

            # 设置产品包装
            if self.udi_data_id.sydycpbs:
                # 避免占用包装的条码
                if self.barcode != self.udi_data_id.sydycpbs:
                    self.barcode = self.udi_data_id.sydycpbs

                product_packaging = self.env['product.packaging'].search([('barcode', '=', self.udi_data_id.zxxsdycpbs)], limit=1)
                if not product_packaging:
                    product_packaging = self.env['product.packaging'].create({
                        'name': '%d %s' % (self.udi_data_id.zxxsdyzsydydsl, self.uom_id.name),
                        'product_id': self.product_variant_id.id,
                        'qty': self.udi_data_id.zxxsdyzsydydsl,
                        'barcode': self.udi_data_id.zxxsdycpbs,
                    })

    @api.onchange('barcode')
    def _barcode_to_udi_data(self):
        # 设置医疗器械唯一标识
        if self.barcode and self.is_medical_consumables:
            udi_data = self.env['udi.data'].search(['|', ('zxxsdycpbs', '=', self.barcode), ('sydycpbs', '=', self.barcode)], limit=1)
            if udi_data:
                self.udi_data_id = udi_data.id
            else:
                return {
                    'warning': {
                        'title': '警告',
                        'message': '未能在医疗器械唯一标识数据库里找到产品标识 %s' % self.barcode,
                    }
                }
