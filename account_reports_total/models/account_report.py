# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _, osv, Command

class AccountReport(models.Model):
    _inherit = "account.report"

    show_daily_total = fields.Boolean(
        string="显示本日合计",
        compute=lambda x: x._compute_report_option_filter('show_daily_total', False), readonly=False, store=True, depends=['root_report_id'],
    )
    show_monthly_total = fields.Boolean(
        string="显示本月合计",
        compute=lambda x: x._compute_report_option_filter('show_monthly_total', False), readonly=False, store=True, depends=['root_report_id'],
    )
    show_yearly_total = fields.Boolean(
        string="显示本年累计",
        compute=lambda x: x._compute_report_option_filter('show_yearly_total', False), readonly=False, store=True, depends=['root_report_id'],
    )

    def _init_options_daily_total(self, options, previous_options=None):
        if self.show_daily_total and previous_options:
            options['daily_total'] = previous_options.get('daily_total', False)
        else:
            options['daily_total'] = False

    def _init_options_monthly_total(self, options, previous_options=None):
        if self.show_monthly_total and previous_options:
            options['monthly_total'] = previous_options.get('monthly_total', False)
        else:
            options['monthly_total'] = False

    def _init_options_yearly_total(self, options, previous_options=None):
        if self.show_yearly_total and previous_options:
            options['yearly_total'] = previous_options.get('yearly_total', False)
        else:
            options['yearly_total'] = False
