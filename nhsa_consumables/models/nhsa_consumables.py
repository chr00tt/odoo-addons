# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class NHSAConsumables(models.Model):
    _name = "nhsa.consumables"
    _description = "医保医用耗材分类与代码"

    name = fields.Char('耗材代码', index='trigram', required=True)

    nhsa_consumables_categ_id = fields.Many2one(
        'nhsa.consumables.category', '耗材分类',
        required=True)
    nhsa_consumables_categ_code = fields.Char('分类码',
        related='nhsa_consumables_categ_id.code')

    common_name = fields.Char('通用名', required=True)
    material = fields.Char('材质', required=True)
    specifications = fields.Char('规格', required=True)
    enterprise = fields.Char('企业', required=True)
