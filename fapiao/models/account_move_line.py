# -*- coding: utf-8 -*-

from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    fapiao_lines = fields.One2many(
        'fapiao.line',
        'move_line_id',
        string='发票明细',
        readonly=True,
        copy=True,
    )

