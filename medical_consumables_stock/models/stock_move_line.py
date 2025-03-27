# -*- coding: utf-8 -*-

from odoo import _, api, fields, tools, models, Command

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    product_ggxh = fields.Char(related="product_id.ggxh")
