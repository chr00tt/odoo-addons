# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons.sale_subscription.models.product import product_template
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    udi_data_id = fields.Many2one('udi.data', '医疗器械唯一标识')

    syqsfxyjxmj = fields.Boolean("使用前是否需要进行灭菌")
    gllb = fields.Selection([('1', 'Ⅰ'), ('2', 'Ⅱ'), ('3', 'Ⅲ')], string='管理类别', default='1')

    udi_flbm = fields.Many2one('medical.device.category', related='udi_data_id.flbm', store=True)

    udi_zxxsdycpbs = fields.Char(related='udi_data_id.zxxsdycpbs')
    udi_sydycpbs = fields.Char(related='udi_data_id.sydycpbs')
    udi_btcpbs = fields.Char(related='udi_data_id.btcpbs')
    udi_cpmctymc = fields.Char(related='udi_data_id.cpmctymc')
    udi_spmc = fields.Char(related='udi_data_id.spmc')
    udi_ggxh = fields.Char(related='udi_data_id.ggxh')

    @api.onchange('udi_data_id')
    def _onchange_udi_data_id(self):
        if self.udi_data_id:
            # 设置医用耗材标志
            self.is_medical_consumables = self.udi_data_id.cplb == '耗材'

            # 设置医保医用耗材代码
            if self.udi_data_id.ybbm and not self.nhsa_consumables_id:
                self.ybbm = self.udi_data_id.ybbm

            # 设置条码
            if not self.barcode:
                self.barcode = self.udi_data_id.sydycpbs if self.udi_data_id.sydycpbs else self.udi_data_id.zxxsdycpbs

            # 设置规格
            if not self.ggxh and self.udi_data_id.ggxh:
                self.ggxh = self.udi_data_id.ggxh

            # 设置追溯
            if self.udi_data_id.serial_number:
                self.tracking = 'serial'
            elif self.udi_data_id.lot_or_batch_number and self.tracking != 'serial':
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

                product_packaging = self.env['product.packaging'].search(
                    [('barcode', '=', self.udi_data_id.zxxsdycpbs)], limit=1)
                if not product_packaging:
                    product_packaging = self.env['product.packaging'].create({
                        'name': '%d %s' % (self.udi_data_id.zxxsdyzsydydsl, self.uom_id.name),
                        'product_id': self.product_variant_id.id,
                        'qty': self.udi_data_id.zxxsdyzsydydsl,
                        'barcode': self.udi_data_id.zxxsdycpbs,
                    })

            # 注册证号
            if self.udi_data_id.registration_number:
                self.registration_number = self.udi_data_id.registration_number
            # 生产厂家
            if self.udi_data_id.license_holder:
                self.manufacturer_id = self.udi_data_id.license_holder.id

    @api.onchange('barcode')
    def _barcode_to_udi_data(self):
        # 设置医疗器械唯一标识
        if self.barcode and self.is_medical_consumables:
            udi_data = self.env['udi.data'].search(
                ['|', ('zxxsdycpbs', '=', self.barcode), ('sydycpbs', '=', self.barcode)], limit=1)
            if udi_data:
                self.udi_data_id = udi_data.id  # 会自动触发 _onchange_udi_data_id
            else:
                self.udi_data_id = None

    @api.model_create_multi
    def create(self, vals_list):
        udi_data_model = self.env['udi.data']
        product_template_model = self.env['product.template']
        for vals in vals_list:
            udi_record = None
            if vals.get('ybbm'):
                # 根据医保编码查找UDI数据
                udi_record = udi_data_model.search([('ybbm', '=', vals.get('ybbm'))], limit=1)
            # 不能根据产品名称+规格型号查询，因为不同厂家的产品会有不同的产品标识.
            # 其他方案：1.注册证号+规格型号; 2.查询产品名称+规格型号+生产厂家
            else:
                if vals.get('registration_number') and vals.get('ggxh'):
                    # 1.注册证号+规格型号
                    registration_number = vals.get('registration_number')
                    ggxh = vals.get('ggxh')
                    if registration_number and ggxh:
                        udi_record = udi_data_model.search([
                            ('registration_number', '=', registration_number),
                            ('ggxh', '=', ggxh)
                        ], limit=1)

                if not udi_record:
                    # 2.查询产品名称+规格型号+生产厂家
                    if vals.get('name') and vals.get('ggxh') and vals.get('manufacturer_id'):
                        udi_record = udi_data_model.search([
                            ('cpmctymc', '=', vals.get('name')),
                            ('ggxh', '=', vals.get('ggxh')),
                            ('license_holder', '=', vals.get('manufacturer_id'))
                        ], limit=1)

            if udi_record:
                # 避免用户错误的重复医保编码导致 barcode 重复
                barcode = udi_record.sydycpbs if udi_record.sydycpbs else udi_record.zxxsdycpbs
                # 搜索数据库记录
                if product_template_model.search([('barcode', '=', barcode)], limit=1):
                    udi_record = None
                # 搜索 vals_list
                match = next((v for v in vals_list if v.get('barcode') == barcode), None)
                if match:
                    udi_record = None

            # 根据药监局数据补充产品属性
            if udi_record:
                vals['udi_data_id'] = udi_record.id

                # 设置医保编码（如果条件满足）
                if udi_record.ybbm:
                    vals['ybbm'] = udi_record.ybbm

                # 设置医用耗材标志
                if udi_record.cplb == '耗材':
                    vals['is_medical_consumables'] = True

                # 设置条码
                if not vals.get('barcode'):
                    vals['barcode'] = udi_record.sydycpbs if udi_record.sydycpbs else udi_record.zxxsdycpbs

                # 设置规格
                if not vals.get('ggxh') and udi_record.ggxh:
                    vals['ggxh'] = udi_record.ggxh

                # 设置追溯方式
                if udi_record.serial_number:
                    vals['tracking'] = 'serial'

                # 设置内部说明
                if not vals.get('description') and udi_record.cpms:
                    vals['description'] = udi_record.cpms
                # 注册证号
                if udi_record.registration_number:
                    vals['registration_number'] = udi_record.registration_number

                # 生产厂家
                if udi_record.license_holder:
                    vals['manufacturer_id'] = udi_record.license_holder.id

        product_templates = super().create(vals_list)

        # 生成产品包装
        for product_template in product_templates:
            # 确保产品有关联的UDI数据
            if product_template.udi_data_id:
                udi_data = product_template.udi_data_id
                if udi_data.sydycpbs:
                    # 避免占用包装的条码
                    if product_template.barcode != udi_data.sydycpbs:
                        product_template.barcode = udi_data.sydycpbs

                    product_packaging = self.env['product.packaging'].search(
                        [('barcode', '=', udi_data.zxxsdycpbs)], limit=1)
                    if not product_packaging:
                        product_packaging = self.env['product.packaging'].create({
                            'name': '%d %s' % (udi_data.zxxsdyzsydydsl, product_template.uom_id.name),
                            'product_id': product_template.product_variant_id.id,
                            'qty': udi_data.zxxsdyzsydydsl,
                            'barcode': udi_data.zxxsdycpbs,
                        })
        return product_templates
