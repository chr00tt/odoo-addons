# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    production_date = fields.Datetime(
        string='生产日期', compute='_compute_production_date', store=True)

    @api.depends('product_id', 'lot_id.production_date')
    def _compute_production_date(self):
        for move_line in self:
            if move_line.lot_id.production_date:
                move_line.production_date = move_line.lot_id.production_date
            elif move_line.production_date:
                continue
            else:
                move_line.production_date = False

    def _get_fields_stock_barcode(self):
        return super()._get_fields_stock_barcode() + ['production_date']

