# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_medical_consumables = fields.Boolean('医用耗材', compute='_compute_is_medical_consumables',
        store=True, readonly=False)

    ggxh = fields.Char("规格/型号")
    ybbm = fields.Char("医保耗材编码")

    registration_number = fields.Char("注册证编号或者备案凭证编号")
    product_origin = fields.Selection([
        ('domestic', '国产'),
        ('imported', '进口'),
        ('hongkong_macao_taiwan', '港澳台'),
    ], string='产品来源', default='domestic')

    @api.depends('type')
    def _compute_is_medical_consumables(self):
        self.filtered(lambda p: p.type not in ['product']).update({'is_medical_consumables': False})
