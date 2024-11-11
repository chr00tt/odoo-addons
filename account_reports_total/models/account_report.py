# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _, osv, Command

class AccountReport(models.Model):
    _inherit = "account.report"

    daily_total = fields.Boolean(
        string="本日合计",
        compute=lambda x: x._compute_report_option_filter('daily_total'), readonly=False, store=True, depends=['root_report_id'],
    )
    monthly_total = fields.Boolean(
        string="本月合计",
        compute=lambda x: x._compute_report_option_filter('monthly_total'), readonly=False, store=True, depends=['root_report_id'],
    )
    accumulative_total = fields.Boolean(
        string="本年累计",
        compute=lambda x: x._compute_report_option_filter('accumulative_total'), readonly=False, store=True, depends=['root_report_id'],
    )
