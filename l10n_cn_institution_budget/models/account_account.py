# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools

class AccountAccount(models.Model):
    _inherit = "account.account"

    is_budget = fields.Boolean("预算会计", compute='_compute_is_budget', store=True)

    @api.depends('code')
    def _compute_is_budget(self):
        for record in self:
            if record.code:
                code = record.code[:1]
                record.is_budget = code in ['6', '7', '8']
            else:
                record.is_budget = False
