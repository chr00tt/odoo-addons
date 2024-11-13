# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import copy

from odoo import models, fields, api, _
from odoo.tools.misc import format_date
from odoo.exceptions import UserError

class GeneralLedgerCustomHandler(models.AbstractModel):
    _inherit = 'account.general.ledger.report.handler'

    def _get_aml_line(self, report, parent_line_id, options, eval_dict, init_bal_by_col_group):
        line_columns = []
        for column in options['columns']:
            col_expr_label = column['expression_label']
            col_value = eval_dict[column['column_group_key']].get(col_expr_label)

            if col_value is None:
                line_columns.append({})
            else:
                col_class = 'number'

                if col_expr_label == 'amount_currency':
                    currency = self.env['res.currency'].browse(eval_dict[column['column_group_key']]['currency_id'])

                    if currency != self.env.company.currency_id:
                        formatted_value = report.format_value(col_value, currency=currency, figure_type=column['figure_type'], blank_if_zero=column['blank_if_zero'])
                    else:
                        formatted_value = ''
                elif col_expr_label == 'date':
                    formatted_value = format_date(self.env, col_value)
                    col_class = 'date'
                elif col_expr_label == 'balance':
                    # 取余额数据
                    col_value += init_bal_by_col_group['balance'][column['column_group_key']] if 'balance' in init_bal_by_col_group else 0
                    formatted_value = report.format_value(col_value, figure_type=column['figure_type'], blank_if_zero=False)
                elif col_expr_label == 'communication' or col_expr_label == 'partner_name':
                    col_class = 'o_account_report_line_ellipsis'
                    formatted_value = report.format_value(col_value, figure_type=column['figure_type'])
                else:
                    formatted_value = report.format_value(col_value, figure_type=column['figure_type'], blank_if_zero=column['blank_if_zero'])
                    if col_expr_label not in ('debit', 'credit'):
                        col_class = ''

                line_columns.append({
                    'name': formatted_value,
                    'no_format': col_value,
                    'class': col_class,
                })

        aml_id = None
        move_name = None
        caret_type = None
        for column_group_dict in eval_dict.values():
            aml_id = column_group_dict.get('id', '')
            if aml_id:
                if column_group_dict.get('payment_id'):
                    caret_type = 'account.payment'
                else:
                    caret_type = 'account.move.line'
                move_name = column_group_dict['move_name']
                date = str(column_group_dict.get('date', ''))
                break

        return {
            'id': report._get_generic_line_id('account.move.line', aml_id, parent_line_id=parent_line_id, markup=date),
            'caret_options': caret_type,
            'parent_id': parent_line_id,
            'name': move_name,
            'columns': line_columns,
            'level': 2,
        }
    
    def _get_periodic_total_line(self, report, parent_line_id, options, init_bal_by_col_group, balance, title, type):
        line_columns = []
        for column in options['columns']:
            col_expr_label = column['expression_label']

            if col_expr_label == 'communication':
                col_class = 'o_account_report_line_ellipsis'
                col_value = title
                formatted_value = report.format_value(col_value, figure_type=column['figure_type'])
            elif col_expr_label == 'balance':
                col_value = balance
                formatted_value = report.format_value(col_value, figure_type=column['figure_type'], blank_if_zero=False)
            elif col_expr_label == 'debit':
                col_class = 'number'
                col_value = init_bal_by_col_group['%s_debit' % type][column['column_group_key']]
                formatted_value = report.format_value(col_value, figure_type=column['figure_type'], blank_if_zero=column['blank_if_zero'])
            elif col_expr_label == 'credit':
                col_class = 'number'
                col_value = init_bal_by_col_group['%s_credit' % type][column['column_group_key']]
                formatted_value = report.format_value(col_value, figure_type=column['figure_type'], blank_if_zero=column['blank_if_zero'])
            else:
                line_columns.append({})
                continue

            line_columns.append({
                'name': formatted_value,
                'no_format': col_value,
                'class': col_class,
            })

        return {
            'id': None,
            'caret_options': None,
            'parent_id': parent_line_id,
            'name': '',
            'columns': line_columns,
            'level': 2,
        }

    def _get_daily_total_line(self, report, parent_line_id, options, init_bal_by_col_group, balance):
        return self._get_periodic_total_line(report, parent_line_id, options, init_bal_by_col_group, balance, '本日合计', 'daily')

    def _get_monthly_total_line(self, report, parent_line_id, options, init_bal_by_col_group, balance):
        return self._get_periodic_total_line(report, parent_line_id, options, init_bal_by_col_group, balance, '当前合计', 'monthly')

    def _get_yearly_total_line(self, report, parent_line_id, options, init_bal_by_col_group, balance):
        return self._get_periodic_total_line(report, parent_line_id, options, init_bal_by_col_group, balance, '当前累计', 'yearly')

    def _add_period_total_lines(self, line_dict_id, groupby, options, progress, offset, unfold_all_batch_data, new_line, balance, lines):
        report = self.env.ref('account_reports.general_ledger_report')

        [date_column] = [column
            for column in options['columns']
            if column['expression_label'] == 'date']
        [line_date] = [line_col.get('no_format').strftime('%Y-%m-%d')
            for column, line_col in zip(options['columns'], new_line['columns'])
            if column['expression_label'] == 'date']
        progress_date = progress['date'][date_column['column_group_key']] if 'date' in progress else ''

        if progress_date:
            # 本日合计
            if options['daily_total'] and line_date != progress_date:
                total_line = self._get_daily_total_line(report, line_dict_id, options, progress, balance)
                lines.append(total_line)
            # 本月合计
            if options['monthly_total'] and line_date[:7] != progress_date[:7]:
                total_line = self._get_monthly_total_line(report, line_dict_id, options, progress, balance)
                lines.append(total_line)
            # 本年累计
            if options['yearly_total'] and line_date[:7] != progress_date[:7]:
                total_line = self._get_yearly_total_line(report, line_dict_id, options, progress, balance)
                lines.append(total_line)

    def _report_expand_unfoldable_line_general_ledger(self, line_dict_id, groupby, options, progress, offset, unfold_all_batch_data=None):
        def init_load_more_progress(line_dict, progress=None):
            # 保存余额、本日合计、本月合计、本年累计
            result = {
                'balance': {
                    column['column_group_key']: line_col.get('no_format', 0)
                    for column, line_col in  zip(options['columns'], line_dict['columns'])
                    if column['expression_label'] == 'balance'
                },
            }
            if not options['daily_total'] and not options['monthly_total'] and not options['yearly_total']:
                return result

            daily_debit = 0
            daily_credit = 0
            monthly_debit = 0
            monthly_credit = 0
            yearly_debit = 0
            yearly_credit = 0

            [date_column] = [column
                for column in options['columns']
                if column['expression_label'] == 'date']
            if progress:
                result.update({
                    'date': {
                        column['column_group_key']: line_col.get('no_format').strftime("%Y-%m-%d")
                        for column, line_col in  zip(options['columns'], line_dict['columns'])
                        if column['expression_label'] == 'date'
                    },
                })
            else:
                result.update({
                    'date': {
                        date_column['column_group_key']: ''
                    },
                })

            if progress:
                [debit_column] = [column
                    for column in options['columns']
                    if column['expression_label'] == 'debit']
                [credit_column] = [column
                    for column in options['columns']
                    if column['expression_label'] == 'credit']

                progress_date = progress['date'][date_column['column_group_key']] if 'date' in progress else ''
                result_date = result['date'][date_column['column_group_key']]

                if progress_date == result_date:
                    daily_debit = progress['daily_debit'][debit_column['column_group_key']]
                    daily_credit = progress['daily_credit'][credit_column['column_group_key']]
                if progress_date[:7] == result_date[:7]:
                    monthly_debit = progress['monthly_debit'][debit_column['column_group_key']]
                    monthly_credit = progress['monthly_credit'][credit_column['column_group_key']]
                if progress_date[:4] == result_date[:4]:
                    yearly_debit = progress['yearly_debit'][debit_column['column_group_key']]
                    yearly_credit = progress['yearly_credit'][credit_column['column_group_key']]

            result.update({
                'daily_debit': {
                    column['column_group_key']: line_col.get('no_format', 0) + daily_debit
                    for column, line_col in  zip(options['columns'], line_dict['columns'])
                    if column['expression_label'] == 'debit'
                },
                'daily_credit': {
                    column['column_group_key']: line_col.get('no_format', 0) + daily_credit
                    for column, line_col in  zip(options['columns'], line_dict['columns'])
                    if column['expression_label'] == 'credit'
                },
                'monthly_debit': {
                    column['column_group_key']: line_col.get('no_format', 0) + monthly_debit
                    for column, line_col in  zip(options['columns'], line_dict['columns'])
                    if column['expression_label'] == 'debit'
                },
                'monthly_credit': {
                    column['column_group_key']: line_col.get('no_format', 0) + monthly_credit
                    for column, line_col in  zip(options['columns'], line_dict['columns'])
                    if column['expression_label'] == 'credit'
                },
                'yearly_debit': {
                    column['column_group_key']: line_col.get('no_format', 0) + yearly_debit
                    for column, line_col in  zip(options['columns'], line_dict['columns'])
                    if column['expression_label'] == 'debit'
                },
                'yearly_credit': {
                    column['column_group_key']: line_col.get('no_format', 0) + yearly_credit
                    for column, line_col in  zip(options['columns'], line_dict['columns'])
                    if column['expression_label'] == 'credit'
                },
            })
            return result

        report = self.env.ref('account_reports.general_ledger_report')
        model, model_id = report._get_model_info_from_id(line_dict_id)

        if model != 'account.account':
            raise UserError(_("Wrong ID for general ledger line to expand: %s", line_dict_id))

        lines = []

        # Get initial balance
        if offset == 0:
            if unfold_all_batch_data:
                account, init_balance_by_col_group = unfold_all_batch_data['initial_balances'][model_id]
            else:
                account, init_balance_by_col_group = self._get_initial_balance_values(report, [model_id], options)[model_id]

            initial_balance_line = report._get_partner_and_general_ledger_initial_balance_line(options, line_dict_id, init_balance_by_col_group, account.currency_id)

            if initial_balance_line:
                lines.append(initial_balance_line)

                # For the first expansion of the line, the initial balance line gives the progress
                progress = init_load_more_progress(initial_balance_line)

        # Get move lines
        limit_to_load = report.load_more_limit + 1 if report.load_more_limit and not self._context.get('print_mode') else None
        if unfold_all_batch_data:
            aml_results = unfold_all_batch_data['aml_results'][model_id]
            has_more = unfold_all_batch_data['has_more'].get(model_id, False)
        else:
            aml_results, has_more = self._get_aml_values(report, options, [model_id], offset=offset, limit=limit_to_load)
            aml_results = aml_results[model_id]

        next_progress = progress
        for aml_result in aml_results.values():
            # 保存计算前的余额
            [balance_column] = [column
                for column in options['columns']
                if column['expression_label'] == 'balance']
            balance = next_progress['balance'][balance_column['column_group_key']] if 'balance' in next_progress else 0

            new_line = self._get_aml_line(report, line_dict_id, options, aml_result, next_progress)

            # 添加本日合计、本月合计、本年累计行
            if options['daily_total'] or options['monthly_total'] or options['yearly_total']:
                self._add_period_total_lines(line_dict_id, groupby, options, next_progress, offset, unfold_all_batch_data, new_line, balance, lines)

            lines.append(new_line)
            next_progress = init_load_more_progress(new_line, next_progress)

        return {
            'lines': lines,
            'offset_increment': report.load_more_limit,
            'has_more': has_more,
            'progress': json.dumps(next_progress),
        }
