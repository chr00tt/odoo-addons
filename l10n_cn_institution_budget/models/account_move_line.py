# -*- coding: utf-8 -*-

from odoo import api, fields, models, Command, _

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_budget = fields.Boolean("预算会计")
