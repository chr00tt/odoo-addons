# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class NHSAConsumables(models.Model):
    _name = "nhsa.consumables"
    _description = "医保医用耗材分类与代码"

    name = fields.Char('耗材代码', index='trigram', required=True)
    primary = fields.Char('一级分类', required=True)
    secondary = fields.Char('二级分类', required=True)
    tertiary = fields.Char('三级分类', required=True)
    common_name = fields.Char('通用名', required=True)
    material = fields.Char('材质', required=True)
    specifications = fields.Char('规格', required=True)
    enterprise = fields.Char('企业', required=True)
