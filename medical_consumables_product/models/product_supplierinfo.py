# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    product_ggxh = fields.Char('规格/型号', related="product_tmpl_id.ggxh")
    registration_number = fields.Char('注册证号', related="product_tmpl_id.registration_number")
    manufacturer_id = fields.Many2one('res.partner', '生产厂家', related="product_tmpl_id.manufacturer_id")
    ybbm = fields.Char('医保编码', related="product_tmpl_id.ybbm")
