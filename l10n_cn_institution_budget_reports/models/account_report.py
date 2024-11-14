# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _, osv, _lt

class AccountReport(models.Model):
    _inherit = 'account.report'

    def _get_options(self, previous_options=None):
        options = super(AccountReport, self)._get_options(previous_options)

        options['financial_account'] = (previous_options or {}).get('financial_account', False)
        options['budget_account'] = (previous_options or {}).get('budget_account', False)

        return options

    def _get_options_domain(self, options, date_scope):
        domain = super(AccountReport, self)._get_options_domain(options, date_scope)

        financial_account = options.get('financial_account')
        budget_account = options.get('budget_account')
        if financial_account != budget_account:
            domain += [('account_id.is_budget', '=', budget_account)]

        return domain
