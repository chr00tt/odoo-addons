# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json

from odoo import models, _
from odoo.exceptions import UserError
from odoo.tools import format_date, date_utils, get_lang

class AnalyticReportHandler(models.AbstractModel):
    _name = 'account.analytic.report.handler'
    _inherit = 'account.report.custom.handler'

    def _dynamic_lines_generator(self, report, options, all_column_groups_expression_totals):
        analytic_plan_lines = self._build_analytic_plan_lines(report, options)
        lines = report._regroup_lines_by_name_prefix(options, analytic_plan_lines, '_report_expand_analytic_plan', 0)

        # Inject sequence on dynamic lines
        lines = [(0, line) for line in lines]

        return lines

    def _build_analytic_plan_lines(self, report, options):
        lines = []

        for analytic_plan in self._query_analytic_plans(options):
            lines.append(self._get_report_line_analytic_plans(options, analytic_plan))

        return lines

    def _query_analytic_plans(self, options):
        analytic_plans = self.env['account.analytic.plan'].search([])
        return [(analytic_plan) for analytic_plan in analytic_plans]

    def _report_expand_unfoldable_line_analytic_plan_ledger(self, line_dict_id, groupby, options, progress, offset, unfold_all_batch_data=None):
        lines = []

        report = self.env.ref('account_analytic_report.analytic_report')
        markup, model, record_id = report._parse_line_id(line_dict_id)[-1]

        if model != 'account.analytic.plan':
            raise UserError(_("Wrong ID for analytic line to expand: %s", line_dict_id))

        analytic_accounts = self.env['account.analytic.account'].search([('plan_id', '=', record_id)])
        for analytic_account in analytic_accounts:
            lines.append(self._get_report_line_analytic_account(options, line_dict_id, analytic_account, 1))

        return {
            'lines': lines,
        }

    def _get_report_line_analytic_account(self, options, parent_line_id, analytic_account, level_shift=0):
        company_currency = self.env.company.currency_id
        unfold_all = (self._context.get('print_mode') and not options.get('unfolded_lines')) or options.get('unfold_all')

        column_values = []
        report = self.env['account.report']

        line_id = report._get_generic_line_id('account.analytic.account', analytic_account.id) if analytic_account else report._get_generic_line_id('account.analytic.account', None, markup='no_analytic_account')

        return {
            'id': line_id,
            'name': analytic_account is not None and (analytic_account.name or '')[:128] or self._get_no_analytic_account_line_label(),
            'columns': column_values,
            'level': 2 + level_shift,
            'parent_id': parent_line_id,
            'unfoldable': True,
            'unfolded': line_id in options['unfolded_lines'] or unfold_all,
            'expand_function': '_report_expand_unfoldable_line_analytic_account_ledger',
        }

    def _get_report_line_analytic_plans(self, options, analytic_plan, level_shift=0):
        company_currency = self.env.company.currency_id
        unfold_all = (self._context.get('print_mode') and not options.get('unfolded_lines')) or options.get('unfold_all')

        column_values = []
        report = self.env['account.report']

        line_id = report._get_generic_line_id('account.analytic.plan', analytic_plan.id) if analytic_plan else report._get_generic_line_id('account.analytic.plan', None, markup='no_analytic_plan')

        return {
            'id': line_id,
            'name': analytic_plan is not None and (analytic_plan.name or '')[:128] or self._get_no_analytic_plan_line_label(),
            'columns': column_values,
            'level': 2 + level_shift,
            'unfoldable': True,
            'unfolded': line_id in options['unfolded_lines'] or unfold_all,
            'expand_function': '_report_expand_unfoldable_line_analytic_plan_ledger',
        }
