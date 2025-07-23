# -*- coding: utf-8 -*-

from odoo import api, fields, models

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_ggxh = fields.Char(related='product_id.ggxh')
    registration_number = fields.Char('注册证号', related='product_id.registration_number')
    manufacturer_id = fields.Many2one(
        'res.partner', string='生产厂家',
        related='product_id.manufacturer_id')

