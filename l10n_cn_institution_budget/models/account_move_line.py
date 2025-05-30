# -*- coding: utf-8 -*-

from odoo import api, fields, models, Command, _
from odoo.exceptions import ValidationError, UserError

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_budget = fields.Boolean("预算会计", default=False)

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

    @api.constrains('account_id', 'tax_ids', 'tax_line_id', 'reconciled')
    def _check_off_balance(self):
        for line in self:
            if line.is_budget:
                continue
            if line.account_id.internal_group == 'off_balance':
                if any(a.internal_group != line.account_id.internal_group for a in line.move_id.line_ids.account_id):
                    raise UserError(_('If you want to use "Off-Balance Sheet" accounts, all the accounts of the journal entry must be of this type'))
                if line.tax_ids or line.tax_line_id:
                    raise UserError(_('You cannot use taxes on lines with an Off-Balance account'))
                if line.reconciled:
                    raise UserError(_('Lines from "Off-Balance Sheet" accounts cannot be reconciled'))
