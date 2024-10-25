# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, Command

class AccountMove(models.Model):
    _inherit = "account.move"

    line_ids = fields.One2many(
        'account.move.line',
        'move_id',
        string='财务会计项目',
        copy=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        domain="[('is_budget', '!=', True)]",
        context="{'default_is_budget': False}"
    )

    budget_line_ids = fields.One2many(
        'account.move.line',
        'move_id',
        string='预算会计项目',
        copy=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        domain="[('is_budget', '=', True)]",
        context="{'default_is_budget': True}"
    )
