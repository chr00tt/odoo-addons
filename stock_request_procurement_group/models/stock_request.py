# -*- coding: utf-8 -*-

from odoo import api, fields, models

class StockRequest(models.Model):
    _inherit = "stock.request"

    def action_confirm(self):
        if not self.procurement_group_id:
            self.procurement_group_id = self.procurement_group_id.create({
                'name': self.name,
                'stock_request_id': self.id,
            })

        return super(StockRequest, self).action_confirm()