# -*- encoding: utf-8 -*-

from odoo import _, api, fields, models

class StockRequestOrder(models.Model):
    _name = "stock.request.order"
    _inherit = ["stock.request.order", "tier.validation"]
    _state_from = ["draft"]
    _state_to = ["open"]

    _tier_validation_manual_config = False
