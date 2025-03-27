# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _, SUPERUSER_ID

class ProductTemplate(models.Model):
    _inherit = "product.template"

    nhsa_consumables_id = fields.Many2one('nhsa.consumables', '医保代码')

    nhsa_consumables_categ_id = fields.Many2one('nhsa.consumables.category', '医保耗材分类', related='nhsa_consumables_id.nhsa_consumables_categ_id', store=True)
    nhsa_common_name = fields.Char('医保通用名', related='nhsa_consumables_id.common_name')
    nhsa_material = fields.Char('医保材质', related='nhsa_consumables_id.material')
    nhsa_specifications = fields.Char('医保规格', related='nhsa_consumables_id.specifications')
