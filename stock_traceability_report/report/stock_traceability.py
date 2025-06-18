# -*- coding: utf-8 -*-

from odoo import api, models, _

class MrpStockReport(models.TransientModel):
    _inherit = 'stock.traceability.report'

    def _get_main_lines(self):
        context = dict(self.env.context)
        return {'lines': self.with_context(context).get_lines()}
