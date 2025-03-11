# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _

class UDIData(models.Model):
    _name = "udi.data"
    _inherit = ['rss.mixin']
    _description = "医疗器械唯一标识"

    zxxsdycpbs = fields.Char("最小销售单元产品标识")
    cpbsbmtxmc = fields.Char("产品标识编码体系名称")
    cpbsfbrq = fields.Char("产品标识发布日期")
    zxxsdyzsydydsl = fields.Integer("最小销售单元中使用单元的数量")
    sydycpbs = fields.Boolean("使用单元产品标识")
    cpmctymc = fields.Char("产品名称/通用名称")
    spmc = fields.Char("商品名称")
    ggxh = fields.Char("型号规格/包装规格")
    sfwblztlcp = fields.Boolean("是否为包类/组套类产品")
    cpms = fields.Text("产品描述")
    cphhhbh = fields.Char("产品货号或编号")
    yflbm = fields.Char("原器械目录代码")
    #qxlb = fields.Char("器械类别")
    flbm = fields.Char("分类编码")
    ylqxzcrbarmc = fields.Char("医疗器械注册人/备案人名称")
    ylqxzcrbarywmc = fields.Char("医疗器械注册人/备案人英文名称")
    tyshxydm = fields.Char("统一社会信息代码")
    zczbhhzbapzbh = fields.Char("注册证编号或者备案凭证编号")
    ybbm = fields.Char("医保耗材分类编码")
    cplb = fields.Char("产品类别")
    cgzmraqxgxx = fields.Char("磁共振（MR）安全相关信息")
    sfbjwycxsy = fields.Boolean("是否标记为一次性使用")
    zdcfsycs = fields.Integer("最大重复使用次数")
    sfwwjbz = fields.Boolean("是否为无菌包装")
    syqsfxyjxmj = fields.Boolean("使用前是否需要进行灭菌")
    mjfs = fields.Text("灭菌方式")
    deviceRecordKey = fields.Char("主键编号")
    versionNumber = fields.Integer("公开的版本号")
    tsrq = fields.Char("退市日期")
    versionTime = fields.Char("版本日期")

