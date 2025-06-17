# -*- coding: utf-8 -*-

from odoo import api, fields, models

class StockRequestOrder(models.Model):
    _inherit = "stock.request.order"

    def action_confirm(self):
        if not self.procurement_group_id:
            self.procurement_group_id = self.procurement_group_id.create({
                'name': self.name,
                'stock_request_order_id': self.id,
            })
            self.change_childs()

        return super(StockRequestOrder, self).action_confirm()
