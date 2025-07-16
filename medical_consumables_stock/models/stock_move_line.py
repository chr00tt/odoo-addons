# -*- coding: utf-8 -*-

from odoo import _, api, fields, tools, models, Command

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    product_ggxh = fields.Char(related="product_id.ggxh")
    registration_number = fields.Char('注册证号', related="product_id.registration_number")
    product_tag_ids = fields.Many2many(
        'product.tag', string='产品标签',
        related='product_id.product_tag_ids')
    manufacturer_id = fields.Many2one(
        'res.partner', string='生产厂家',
        related='product_id.manufacturer_id')
    categ_id = fields.Many2one(
        'product.category', string='产品类别',
        related='product_id.categ_id')
    product_ybbm = fields.Char(related="product_id.ybbm")
