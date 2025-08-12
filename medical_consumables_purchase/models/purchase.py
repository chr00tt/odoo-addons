# -*- coding: utf-8 -*-

from odoo import fields, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_ggxh = fields.Char(related="product_id.ggxh")
    registration_number = fields.Char('注册证号', related="product_id.registration_number")
    registration_start_date = fields.Date(related="product_id.registration_start_date")
    registration_validity_period = fields.Date(related="product_id.registration_validity_period")
    manufacturer_id = fields.Many2one(string="生产厂家", related="product_id.manufacturer_id")
    ybbm = fields.Char(related="product_id.ybbm")
