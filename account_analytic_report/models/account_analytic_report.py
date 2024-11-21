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


        partner_lines, totals_by_column_group = self._build_analytic_account_lines(report, options, record_id)
        lines = report._regroup_lines_by_name_prefix(options, partner_lines, '_report_expand_unfoldable_line_partner_ledger_prefix_group', 0)

        analytic_accounts = self.env['account.analytic.account'].search([('plan_id', '=', record_id)])
        for analytic_account in analytic_accounts:
            lines.append(self._get_report_line_analytic_account(options, line_dict_id, analytic_account, 1))

        return {
            'lines': lines,
        }

    def _build_partner_lines(self, report, options, analytic_plan_id, level_shift=0):
        lines = []

        totals_by_column_group = {
            column_group_key: {
                total: 0.0
                for total in ['debit', 'credit', 'balance']
            }
            for column_group_key in options['column_groups']
        }

        for partner, results in self._query_analytic_accounts(options, analytic_plan_id):
            if not partner:
                continue

            partner_values = defaultdict(dict)
            for column_group_key in options['column_groups']:
                partner_sum = results.get(column_group_key, {})

                partner_values[column_group_key]['debit'] = partner_sum.get('debit', 0.0)
                partner_values[column_group_key]['credit'] = partner_sum.get('credit', 0.0)
                partner_values[column_group_key]['balance'] = partner_sum.get('balance', 0.0)

                totals_by_column_group[column_group_key]['debit'] += partner_values[column_group_key]['debit']
                totals_by_column_group[column_group_key]['credit'] += partner_values[column_group_key]['credit']
                totals_by_column_group[column_group_key]['balance'] += partner_values[column_group_key]['balance']

            lines.append(self._get_report_line_analytic_accounts(options, partner, partner_values, level_shift=level_shift))

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
        query, params = self._get_query_sums(options)

        groupby_partners = {}

        self._cr.execute(query, params)
        for res in self._cr.dictfetchall():
            assign_sum(res)

        # Correct the sums per partner, for the lines without partner reconciled with a line having a partner
        query, params = self._get_sums_without_partner(options)

        self._cr.execute(query, params)
        totals = {}
        for total_field in ['debit', 'credit', 'balance']:
            totals[total_field] = {col_group_key: 0 for col_group_key in options['column_groups']}

        for row in self._cr.dictfetchall():
            totals['debit'][row['column_group_key']] += row['debit']
            totals['credit'][row['column_group_key']] += row['credit']
            totals['balance'][row['column_group_key']] += row['balance']

            if row['groupby'] not in groupby_partners:
                continue

            assign_sum(row)

        if None in groupby_partners:
            # Debit/credit are inverted for the unknown partner as the computation is made regarding the balance of the known partner
            for column_group_key in options['column_groups']:
                groupby_partners[None][column_group_key]['debit'] += totals['credit'][column_group_key]
                groupby_partners[None][column_group_key]['credit'] += totals['debit'][column_group_key]
                groupby_partners[None][column_group_key]['balance'] -= totals['balance'][column_group_key]

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
