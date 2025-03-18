# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

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
    flbm = fields.Many2one('medical.device.category', '分类编码')
    tyshxydm = fields.Char("统一社会信息代码")
    zczbhhzbapzbh = fields.Char("注册证编号或者备案凭证编号")
    ylqxzcrbarmc = fields.Char("医疗器械注册人/备案人名称")
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

    gllb = fields.Selection('管理类别', related='flbm.gllb', store=True)

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
        product_template_ids = self.env['product.template'].search([('udi_data_id', 'in', self.ids)])
        data = dict((record.udi_data_id.id, record.id) for record in product_template_ids)
        for record in self:
            record.product_template_id = data.get(record.id, None)

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
        name = self.spmc
        if not name:
            name = self.cpmctymc
            if self.ggxh:
                name += ' ' + self.ggxh
        values = {
            'name': name,
            'is_medical_consumables': True,
            'detailed_type': 'product',

            'specifications': self.ggxh,
            'default_code': self.zxxsdycpbs,
            'barcode': self.sydycpbs if self.sydycpbs else self.zxxsdycpbs,
            'description': self.cpms,
            'tracking': 'serial' if self.scbssfbhxlh else 'lot',
            'use_expiration_date': self.scbssfbhsxrq,

            'udi_data_id': self.id,
            'nhsa_consumables_id': self.nhsa_consumables_id.id if self.nhsa_consumables_id else None,
        }
        return values

    def action_generate_product(self):
        vals_list = []
        for record in self:
            if not record.product_template_id:
                vals_list.append(record._get_product_template_values())
        self.env['product.template'].create(vals_list)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '生成产品',
                'message': '已成功生成 %s 个产品.' % len(vals_list),
                'type': 'success',
            }
        }
