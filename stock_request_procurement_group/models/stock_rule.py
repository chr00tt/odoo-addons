# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    stock_request_order_id = fields.Many2one('stock.request.order', '库存申请单')
    stock_request_id = fields.Many2one('stock.request', '库存申请')
