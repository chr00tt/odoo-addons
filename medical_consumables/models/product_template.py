# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_medical_consumables = fields.Boolean('医用耗材', compute='_compute_is_medical_consumables',
        store=True, readonly=False)

    @api.depends('type')
    def _compute_is_medical_consumables(self):
        self.filtered(lambda p: p.type not in ['product']).update({'is_medical_consumables': False})
