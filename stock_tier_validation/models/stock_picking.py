# -*- encoding: utf-8 -*-

from odoo import api, fields, models

class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "tier.validation"]
    _state_from = ["assigned"]
    _state_to = ["done"]

    _tier_validation_manual_config = False

    def button_validate(self):
        vals = {"state": "done"}

        # 检查是否需要审批
        self._tier_validation_check_state_on_write(vals)
        self._tier_validation_check_write_allowed(vals)
        self._tier_validation_check_write_remove_reviews(vals)

        return super().button_validate()