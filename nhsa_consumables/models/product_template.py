# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _, SUPERUSER_ID

class ProductTemplate(models.Model):
    _inherit = "product.template"

    nhsa_consumables_id = fields.Many2one('nhsa.consumables', '医保代码')

    nhsa_consumables_categ_id = fields.Many2one(related='nhsa_consumables_id.nhsa_consumables_categ_id', store=True)
    common_name = fields.Char(related='nhsa_consumables_id.common_name')
    material = fields.Char(related='nhsa_consumables_id.material')
    specifications = fields.Char(related='nhsa_consumables_id.specifications')
