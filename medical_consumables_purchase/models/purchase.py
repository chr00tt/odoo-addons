# -*- coding: utf-8 -*-

from odoo import fields, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_ggxh = fields.Char(related="product_id.ggxh")
