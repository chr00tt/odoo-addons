# -*- encoding: utf-8 -*-

from odoo import _, api, fields, models

class TierDefinition(models.Model):
    _inherit = "tier.definition"

    @api.model
    def _get_tier_validation_model_names(self):
        res = super()._get_tier_validation_model_names()
        res.append("stock.request.order")
        res.append("stock.request")
        res.append("stock.picking")
        return res
