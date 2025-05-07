# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class UDIData(models.Model):
    _name = "udi.data"
    _inherit = ['rss.mixin']
    _description = "医疗器械唯一标识"
    _rec_name = 'zxxsdycpbs'
    _rec_names_search = ['zxxsdycpbs', 'sydycpbs', 'btcpbs']
    _order = 'deviceRecordKey desc'

    zxxsdycpbs = fields.Char("最小销售单元产品标识")
    cpbsbmtxmc = fields.Char("产品标识编码体系名称")
    cpbsfbrq = fields.Char("产品标识发布日期")
    zxxsdyzsydydsl = fields.Integer("最小销售单元中使用单元的数量")
    sydycpbs = fields.Char("使用单元产品标识")
    sfybtzjbs = fields.Boolean("是否有医疗器械本体直接标识")
    btcpbsyzxxsdycpbssfyz = fields.Boolean("医疗器械本体产品标识与最小销售单元产品标识是否一致")
    btcpbs = fields.Char("本体产品标识")
    cpmctymc = fields.Char("产品名称/通用名称")
    spmc = fields.Char("商品名称")
    ggxh = fields.Char("型号规格/包装规格")
    sfwblztlcp = fields.Boolean("是否为包类/组套类产品")
    cpms = fields.Text("产品描述")
    cphhhbh = fields.Char("产品货号或编号")
    yflbm = fields.Char("原器械目录代码")
    flbm = fields.Many2one('medical.device.category', '医疗器械分类')
    tyshxydm = fields.Char("统一社会信息代码")
    zczbhhzbapzbh = fields.Char("注册证编号或者备案凭证编号")
    ylqxzcrbarmc = fields.Many2one(
        'res.partner', '医疗器械注册人/备案人名称',
        required=True)
    ylqxzcrbarywmc = fields.Char("医疗器械注册人/备案人英文名称")
    ybbm = fields.Char("医保耗材分类编码")
    cplb = fields.Char("产品类别")
    cgzmraqxgxx = fields.Char("磁共振（MR）安全相关信息")
    sfbjwycxsy = fields.Boolean("是否标记为一次性使用")
    zdcfsycs = fields.Integer("最大重复使用次数")
    sfwwjbz = fields.Boolean("是否为无菌包装")
    syqsfxyjxmj = fields.Boolean("使用前是否需要进行灭菌")
    mjfs = fields.Text("灭菌方式")
    qtxxdwzlj = fields.Text("提供医疗器械其他信息的网址链接")
    tsrq = fields.Char("退市日期")
    scbssfbhph = fields.Boolean("医疗器械生产标识是否包含批号")
    scbssfbhxlh = fields.Boolean("医疗器械生产标识是否包含序列号")
    scbssfbhscrq = fields.Boolean("医疗器械生产标识是否包含生产日期")
    scbssfbhsxrq = fields.Boolean("医疗器械生产标识是否包含失效日期")
    tscchcztj = fields.Char("特殊储存或操作条件")
    tsccsm = fields.Char("特殊尺寸说明")
    deviceRecordKey = fields.Char("主键编号")
    versionNumber = fields.Integer("公开的版本号")
    versionTime = fields.Char("版本日期")

    gllb = fields.Selection(related='flbm.gllb', store=True)

    nhsa_consumables_id = fields.Many2one('nhsa.consumables', '医保医用耗材分类与代码', compute='_compute_nhsa_consumables_id', store=True)

    nhsa_consumables_categ_id = fields.Many2one('nhsa.consumables.category', '医保耗材分类', related='nhsa_consumables_id.nhsa_consumables_categ_id', store=True)
    nhsa_common_name = fields.Char('医保通用名', related='nhsa_consumables_id.common_name')
    nhsa_material = fields.Char('医保材质', related='nhsa_consumables_id.material')
    nhsa_specifications = fields.Char('医保规格', related='nhsa_consumables_id.specifications')

    product_template_id = fields.Many2one('product.template', '产品', compute='_compute_product_template_id')

    @api.depends('ybbm')
    def _compute_nhsa_consumables_id(self):
        for r in self:
            if r.ybbm:
                # 从医保编码截取前20位
                nhsa_consumables_name = r.ybbm[:20]
                nhsa_consumables = self.env['nhsa.consumables'].search([('name', '=', nhsa_consumables_name)], limit=1)
                if nhsa_consumables:
                    r.nhsa_consumables_id = nhsa_consumables.id

    def _compute_product_template_id(self):
        for record in self:
            barcode = self.sydycpbs if self.sydycpbs else self.zxxsdycpbs
            record.product_template_id = self.env['product.template'].search([('barcode', '=', barcode)], limit=1)

    def action_view_product_template(self):
        return {
            'name': '耗材',
            'view_mode': 'form',
            'res_model': 'product.template',
            'type': 'ir.actions.act_window',
            'res_id': self.product_template_id.id,
        }

    def _get_product_template_values(self):
        self.ensure_one()
        barcode = self.sydycpbs if self.sydycpbs else self.zxxsdycpbs
        values = {
            # product 信息
            'name': self.cpmctymc,
            'detailed_type': 'product',
            'default_code': barcode,
            'barcode': barcode,
            'description': self.cpms,
            'tracking': 'serial' if self.scbssfbhxlh else 'lot',
            'use_expiration_date': self.scbssfbhsxrq,

            # product_manufacturer 信息
            'manufacturer_id': self.nhsa_consumables_id.enterprise.id if self.nhsa_consumables_id else self.ylqxzcrbarmc.id,

            # medical_consumables_product 信息
            'is_medical_consumables': True,
            'ggxh': self.ggxh,
            'ybbm': self.ybbm,

            # nhsa_consumables 信息
            'nhsa_consumables_id': self.nhsa_consumables_id.id if self.nhsa_consumables_id else None,

            # udi_data 信息
            'udi_data_id': self.id,
        }
        return values

    def action_generate_product(self):
        product_template_model = self.env['product.template']

        product_count = 0
        package_count = 0
        for record in self:
            barcode = record.sydycpbs if record.sydycpbs else record.zxxsdycpbs
            product_template = product_template_model.search([('barcode', '=', barcode)], limit=1)
            if not product_template:
                product_template = product_template_model.create(record._get_product_template_values())
                product_count += 1

            if barcode != record.zxxsdycpbs:
                product_packaging_model = self.env['product.packaging']
                product_packaging = product_packaging_model.search([('barcode', '=', record.zxxsdycpbs)], limit=1)
                if not product_packaging:
                    product_packaging_model.create({
                        'name': '%d %s' % (record.zxxsdyzsydydsl, product_template.uom_id.name),
                        'product_id': product_template.product_variant_id.id,
                        'qty': record.zxxsdyzsydydsl,
                        'barcode': record.zxxsdycpbs,
                    })
                    package_count += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '生成产品',
                'message': '已成功生成 %s 个产品, %s 个包装.' % (product_count, package_count),
                'type': 'success',
            }
        }

    # 创建 udi.data 后自动关联 product.template
    @api.model_create_multi
    def create(self, vals_list):
        records = super(UDIData, self).create(vals_list)
        for record in records:
            if record.ybbm:
                product_template_model = self.env['product.template']
                product_template = product_template_model.search([('ybbm', '=', record.ybbm)], limit=1)
                if product_template and product_template.udi_data_id.id != record.id:
                    product_template.udi_data_id = record
                    product_template.gllb = record.gllb
                    product_template.barcode = record.sydycpbs if record.sydycpbs else record.zxxsdycpbs
        return records
