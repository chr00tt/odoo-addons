# -*- coding: utf-8 -*-

from odoo import _, api, Command, fields, models

class StockMove(models.Model):
    _inherit = "stock.move"

    product_ggxh = fields.Char(related="product_id.ggxh")
