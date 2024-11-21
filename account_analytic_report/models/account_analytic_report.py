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
        partner_lines = self._build_analytic_plan_lines(report, options)
        lines = report._regroup_lines_by_name_prefix(options, partner_lines, '_report_expand_analytic_plan', 0)

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
        def init_load_more_progress(line_dict):
            return {
                column['column_group_key']: line_col.get('no_format', 0)
                for column, line_col in  zip(options['columns'], line_dict['columns'])
                if column['expression_label'] == 'balance'
            }

        report = self.env.ref('account_reports.analytic_report')
        markup, model, record_id = report._parse_line_id(line_dict_id)[-1]

        if model != 'account.analytic.plan':
            raise UserError(_("Wrong ID for analytic line to expand: %s", line_dict_id))

        prefix_groups_count = 0
        for markup, dummy1, dummy2 in report._parse_line_id(line_dict_id):
            if markup.startswith('groupby_prefix_group:'):
                prefix_groups_count += 1
        level_shift = prefix_groups_count * 2

        lines = []

        # Get initial balance
        if offset == 0:
            if unfold_all_batch_data:
                init_balance_by_col_group = unfold_all_batch_data['initial_balances'][record_id]
            else:
                init_balance_by_col_group = self._get_initial_balance_values([record_id], options)[record_id]
            initial_balance_line = report._get_partner_and_general_ledger_initial_balance_line(options, line_dict_id, init_balance_by_col_group, level_shift=level_shift)
            if initial_balance_line:
                lines.append(initial_balance_line)

                # For the first expansion of the line, the initial balance line gives the progress
                progress = init_load_more_progress(initial_balance_line)

        limit_to_load = report.load_more_limit + 1 if report.load_more_limit and not self._context.get('print_mode') else None

        if unfold_all_batch_data:
            aml_results = unfold_all_batch_data['aml_values'][record_id]
        else:
            aml_results = self._get_aml_values(options, [record_id], offset=offset, limit=limit_to_load)[record_id]

        has_more = False
        treated_results_count = 0
        next_progress = progress
        for result in aml_results:
            if not self._context.get('print_mode') and report.load_more_limit and treated_results_count == report.load_more_limit:
                # We loaded one more than the limit on purpose: this way we know we need a "load more" line
                has_more = True
                break

            new_line = self._get_report_line_move_line(options, result, line_dict_id, next_progress, level_shift=level_shift)
            lines.append(new_line)
            next_progress = init_load_more_progress(new_line)
            treated_results_count += 1

        return {
            'lines': lines,
            'offset_increment': treated_results_count,
            'has_more': has_more,
            'progress': json.dumps(next_progress)
        }

    def _get_report_line_analytic_plans(self, options, analytic_plan, level_shift=0):
        company_currency = self.env.company.currency_id
        unfold_all = (self._context.get('print_mode') and not options.get('unfolded_lines')) or options.get('unfold_all')

        column_values = []
        report = self.env['account.report']

        line_id = report._get_generic_line_id('res.partner', analytic_plan.id) if analytic_plan else report._get_generic_line_id('account.analytic.plan', None, markup='no_analytic_plan')

        return {
            'id': line_id,
            'name': analytic_plan is not None and (analytic_plan.name or '')[:128] or self._get_no_analytic_plan_line_label(),
            'columns': column_values,
            'level': 2 + level_shift,
            'unfoldable': True,
            'unfolded': line_id in options['unfolded_lines'] or unfold_all,
            'expand_function': '_report_expand_unfoldable_line_analytic_plan_ledger',
        }
