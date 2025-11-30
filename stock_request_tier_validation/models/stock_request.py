# -*- encoding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockRequest(models.Model):
    _name = "stock.request"
    _inherit = ["stock.request", "tier.validation"]
    _state_from = ["draft"]
    _state_to = ["open"]

    _tier_validation_manual_config = False

    def action_confirm(self):
        vals = {"state": "open"}

        # 检查是否需要审批
        self._tier_validation_check_state_on_write(vals)
        self._tier_validation_check_write_allowed(vals)
        self._tier_validation_check_write_remove_reviews(vals)

        return super().action_confirm()
    
    # def validate_tier(self):
    #     names = []
    #     for res in self:
    #         if not res.review_ids:
    #             names.append(res.name)
    #     if names:
    #         raise UserError(_("以下订单未提交审批 %s") % ', '.join(names))
    #     return super().validate_tier()