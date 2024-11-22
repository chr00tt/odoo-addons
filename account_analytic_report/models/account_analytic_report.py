# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json

from odoo import models, _
from odoo.exceptions import UserError
from odoo.tools import format_date, date_utils, get_lang

from collections import defaultdict

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


        partner_lines, totals_by_column_group = self._build_analytic_account_lines(report, options, line_dict_id, record_id)
        lines = report._regroup_lines_by_name_prefix(options, partner_lines, '_report_expand_unfoldable_line_partner_ledger_prefix_group', 0)

        return {
            'lines': lines,
        }

    def _build_analytic_account_lines(self, report, options, parent_line_id, analytic_plan_id, level_shift=0):
        lines = []

        totals_by_column_group = {
            column_group_key: {
                total: 0.0
                for total in ['debit', 'credit', 'balance']
            }
            for column_group_key in options['column_groups']
        }

        for analytic_account, results in self._query_analytic_accounts(options, analytic_plan_id):
            if not analytic_account:
                continue

            analytic_account_values = defaultdict(dict)
            for column_group_key in options['column_groups']:
                analytic_account_sum = results.get(column_group_key, {})

                analytic_account_values[column_group_key]['debit'] = analytic_account_sum.get('debit', 0.0)
                analytic_account_values[column_group_key]['credit'] = analytic_account_sum.get('credit', 0.0)
                analytic_account_values[column_group_key]['balance'] = analytic_account_sum.get('balance', 0.0)

                totals_by_column_group[column_group_key]['debit'] += analytic_account_values[column_group_key]['debit']
                totals_by_column_group[column_group_key]['credit'] += analytic_account_values[column_group_key]['credit']
                totals_by_column_group[column_group_key]['balance'] += analytic_account_values[column_group_key]['balance']

            lines.append(self._get_report_line_analytic_accounts(options, analytic_account, analytic_account_values, parent_line_id, level_shift=level_shift))

        return lines, totals_by_column_group

    def _query_analytic_accounts(self, options, analytic_plan_id):
        def assign_sum(row):
            fields_to_assign = ['balance', 'debit', 'credit']
            if any(not company_currency.is_zero(row[field]) for field in fields_to_assign):
                groupby_partners.setdefault(row['groupby'], defaultdict(lambda: defaultdict(float)))
                for field in fields_to_assign:
                    groupby_partners[row['groupby']][row['column_group_key']][field] += row[field]

        company_currency = self.env.company.currency_id

        # Execute the queries and dispatch the results.
        query, params = self._get_query_sums(options, analytic_plan_id)

        groupby_partners = {}

        self._cr.execute(query, params)
        for res in self._cr.dictfetchall():
            assign_sum(res)

        totals = {}
        for total_field in ['debit', 'credit', 'balance']:
            totals[total_field] = {col_group_key: 0 for col_group_key in options['column_groups']}

        # Retrieve the partners to browse.
        # groupby_partners.keys() contains all account ids affected by:
        # - the amls in the current period.
        # - the amls affecting the initial balance.
        if groupby_partners:
            # Note a search is done instead of a browse to preserve the table ordering.
            partners = self.env['res.partner'].with_context(active_test=False, prefetch_fields=False).search([('id', 'in', list(groupby_partners.keys()))])
        else:
            partners = []

        # Add 'Partner Unknown' if needed
        if None in groupby_partners.keys():
            partners = [p for p in partners] + [None]

        return [(partner, groupby_partners[partner.id if partner else None]) for partner in partners]

    def _get_query_sums(self, options, analytic_plan_id):
        """ Construct a query retrieving all the aggregated sums to build the report. It includes:
        - sums for all partners.
        - sums for the initial balances.
        :param options:             The report options.
        :return:                    (query, params)
        """
        params = []
        queries = []
        report = self.env.ref('account_analytic_report.analytic_report')

        # Create the currency table.
        ct_query = self.env['res.currency']._get_query_currency_table(options)
        for column_group_key, column_group_options in report._split_options_per_column_group(options).items():
            column_group_options['analytic_groupby_option'] = True
            tables, where_clause, where_params = report._query_get(column_group_options, 'normal')
            params.append(column_group_key)
            params += where_params
            queries.append(f"""
                SELECT
                    account_analytic_line.account_id                                                      AS groupby,
                    %s                                                                                    AS column_group_key,
                    SUM(ROUND(account_move_line.debit * currency_table.rate, currency_table.precision))   AS debit,
                    SUM(ROUND(account_move_line.credit * currency_table.rate, currency_table.precision))  AS credit,
                    SUM(ROUND(account_move_line.balance * currency_table.rate, currency_table.precision)) AS balance
                FROM {tables}
                LEFT JOIN {ct_query} ON currency_table.company_id = account_move_line.company_id
                LEFT JOIN account_analytic_line ON account_analytic_line.id = account_move_line.id
                LEFT JOIN account_analytic_account ON account_analytic_account.id = account_analytic_line.account_id
                WHERE {where_clause} AND account_analytic_account.plan_id = %s
                GROUP BY account_analytic_line.account_id
            """)
            params += [analytic_plan_id]

        return ' UNION ALL '.join(queries), params

    def _get_report_line_analytic_accounts(self, options, analytic_account, analytic_account_values, parent_line_id, level_shift=0):
        company_currency = self.env.company.currency_id
        unfold_all = (self._context.get('print_mode') and not options.get('unfolded_lines')) or options.get('unfold_all')

        unfoldable = False
        column_values = []
        report = self.env['account.report']
        for column in options['columns']:
            col_expr_label = column['expression_label']
            value = analytic_account_values[column['column_group_key']].get(col_expr_label)

            if col_expr_label in {'debit', 'credit', 'balance'}:
                formatted_value = report.format_value(value, figure_type=column['figure_type'], blank_if_zero=column['blank_if_zero'])
            else:
                formatted_value = report.format_value(value, figure_type=column['figure_type']) if value is not None else value

            unfoldable = unfoldable or (col_expr_label in ('debit', 'credit') and not company_currency.is_zero(value))

            column_values.append({
                'name': formatted_value,
                'no_format': value,
                'class': 'number'
            })

        line_id = report._get_generic_line_id('account.analytic.account', analytic_account.id) if analytic_account else report._get_generic_line_id('account.analytic.account', None, markup='no_analytic_account')

        return {
            'id': line_id,
            'name': analytic_account is not None and (analytic_account.name or '')[:128] or self._get_no_analytic_account_line_label(),
            'columns': column_values,
            'level': 4 + level_shift,
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
