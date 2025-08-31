# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    registration_number = fields.Char('注册证编号或者备案凭证编号', tracking=True)
    registration_start_date = fields.Date('注册证开始日期', tracking=True)
    registration_validity_period = fields.Date('注册证有效期', tracking=True)
