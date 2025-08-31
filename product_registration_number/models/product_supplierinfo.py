# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    registration_number = fields.Char('注册证号', related="product_tmpl_id.registration_number")
    registration_start_date = fields.Date('注册证开始日期', related="product_tmpl_id.registration_start_date")
    registration_validity_period = fields.Date('注册证有效期', related="product_tmpl_id.registration_validity_period")
