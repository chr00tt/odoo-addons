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
    show_accumulative_total = fields.Boolean(
        string="显示本年累计",
        compute=lambda x: x._compute_report_option_filter('show_accumulative_total', False), readonly=False, store=True, depends=['root_report_id'],
    )
