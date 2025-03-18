# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    udi_data_id = fields.Many2one('udi.data', related='product_id.udi_data_id', store=True)

    udi_flbm = fields.Many2one('medical.device.category', related='udi_data_id.flbm')
