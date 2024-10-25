# -*- coding: utf-8 -*-

from odoo import api, fields, models, Command, _

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    account_id = fields.Many2one(
        comodel_name='account.account',
        string='Account',
        compute='_compute_account_id', store=True, readonly=False, precompute=True,
        inverse='_inverse_account_id',
        index=True,
        auto_join=True,
        ondelete="cascade",
        domain=lambda self: [('deprecated', '=', False), ('company_id', '=', self.company_id.id), ('is_off_balance', '=', False), ('is_budget', '=', self.is_budget)],
        check_company=True,
        tracking=True,
    )

    is_budget = fields.Boolean("预算会计", default=False)
