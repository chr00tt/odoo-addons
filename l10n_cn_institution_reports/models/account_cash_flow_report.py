# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountCashFlowReport(models.AbstractModel):
    _name = 'cn_institution.cash.flow.report'
    _inherit = 'account.cash.flow.report'
    _description = '现金流量表'

    @api.model
    def _get_lines(self, options, line_id=None):
        # Compute the cash flow report using the direct method: https://www.investopedia.com/terms/d/direct_method.asp
        lines = []

        layout_data = self._get_layout_data()
        report_data = self._get_report_data(options, layout_data)

        for layout_line_id, layout_line_data in layout_data.items():
            lines.append(self._get_layout_line(options, layout_line_id, layout_line_data, report_data))

            if layout_line_id in report_data and 'aml_groupby_account' in report_data[layout_line_id]:
                aml_data_values = report_data[layout_line_id]['aml_groupby_account'].values()
                for aml_data in sorted(aml_data_values, key=lambda x: x['account_code']):
                    lines.append(self._get_aml_line(options, aml_data))

        unexplained_difference_line = self._get_unexplained_difference_line(options, report_data)

        if unexplained_difference_line:
            lines.append(unexplained_difference_line)

        return lines

    @api.model
    def _get_report_name(self):
        return '现金流量表（行政事业单位）'

    def _get_report_data(self, options, layout_data):
        report_data = {}

        currency_table_query = self._get_query_currency_table(options)

        payment_move_ids, payment_account_ids = self._get_liquidity_move_ids(options)

        # Compute 'Cash and cash equivalents, beginning of period'
        beginning_period_options = self._get_options_beginning_period(options)
        for aml_data in self._compute_liquidity_balance(beginning_period_options, currency_table_query, payment_account_ids):
            self._add_report_data('opening_balance', aml_data, layout_data, report_data)
            self._add_report_data('closing_balance', aml_data, layout_data, report_data)

        # Compute 'Cash and cash equivalents, closing balance'
        for aml_data in self._compute_liquidity_balance(options, currency_table_query, payment_account_ids):
            self._add_report_data('closing_balance', aml_data, layout_data, report_data)

        tags_ids = self._get_tags_ids()
        tags_per_account = self._get_tags_per_account(options, tuple(tags_ids.values()))

        # Process liquidity moves
        res = self._get_liquidity_move_report_lines(options, currency_table_query, payment_move_ids, payment_account_ids)
        for aml_data in res:
            self._dispatch_aml_data(tags_ids, aml_data, layout_data, report_data, tags_per_account)

        # Process reconciled moves
        res = self._get_reconciled_move_report_lines(options, currency_table_query, payment_move_ids, payment_account_ids)
        for aml_data in res:
            self._dispatch_aml_data(tags_ids, aml_data, layout_data, report_data, tags_per_account)

        return report_data

    def _add_report_data(self, layout_line_id, aml_data, layout_data, report_data):
        """
        Add or update the report_data dictionnary with aml_data.

        report_data is a dictionnary where the keys are keys from _cash_flow_report_get_layout_data() (used for mapping)
        and the values can contain 2 dictionnaries:
            * (required) 'balance' where the key is the column_group_key and the value is the balance of the line
            * (optional) 'aml_groupby_account' where the key is an account_id and the values are the aml data
        """
        def _report_update_parent(layout_line_id, aml_balance, layout_data, report_data):
            # Update the balance in report_data of the parent of the layout_line_id recursively (Stops when the line has no parent)
            if 'parent_line_id' in layout_data[layout_line_id]:
                parent_line_id = layout_data[layout_line_id]['parent_line_id']

                report_data.setdefault(parent_line_id, {'balance': 0.0})
                report_data[parent_line_id]['balance'] += aml_balance

                _report_update_parent(parent_line_id, aml_balance, layout_data, report_data)

        aml_account_id, aml_account_code, aml_account_name, aml_balance = aml_data

        if self.env.company.currency_id.is_zero(aml_balance):
            return

        report_data.setdefault(layout_line_id, {
            'balance': 0.0,
            'aml_groupby_account': {},
        })

        report_data[layout_line_id]['aml_groupby_account'].setdefault(aml_account_id, {
            'parent_line_id': layout_line_id,
            'account_id': aml_account_id,
            'account_code': aml_account_code,
            'account_name': aml_account_name,
            'level': layout_data[layout_line_id]['level'] + 1,
            'balance': 0.0,
        })

        report_data[layout_line_id]['balance'] += aml_balance

        report_data[layout_line_id]['aml_groupby_account'][aml_account_id].setdefault('balance', 0.0)
        report_data[layout_line_id]['aml_groupby_account'][aml_account_id]['balance'] += aml_balance

        _report_update_parent(layout_line_id, aml_balance, layout_data, report_data)

    def _get_tags_ids(self):
        ''' Get a dict to pass on to _dispatch_aml_data containing information mapping account tags to report lines. '''
        return {
            'operating_1': self.env.ref('l10n_cn_institution.account_tag_operating_1').id,
            'operating_2': self.env.ref('l10n_cn_institution.account_tag_operating_2').id,
            'operating': self.env.ref('l10n_cn_institution.account_tag_operating').id,
            'operating_4': self.env.ref('l10n_cn_institution.account_tag_operating_4').id,
            'operating_5': self.env.ref('l10n_cn_institution.account_tag_operating_5').id,
            'operating_6': self.env.ref('l10n_cn_institution.account_tag_operating_6').id,
            'investing': self.env.ref('l10n_cn_institution.account_tag_investing').id,
            'investing_1': self.env.ref('l10n_cn_institution.account_tag_investing_1').id,
            'investing_2': self.env.ref('l10n_cn_institution.account_tag_investing_2').id,
            'investing_3': self.env.ref('l10n_cn_institution.account_tag_investing_3').id,
            'investing_4': self.env.ref('l10n_cn_institution.account_tag_investing_4').id,
            'financing': self.env.ref('account.account_tag_financing').id,
        }

    def _dispatch_aml_data(self, tags_ids, aml_data, layout_data, report_data, tags_per_account):
        account_id, account_code, account_name, account_internal_type, amount = aml_data
        aml_data = (account_id, account_code, account_name, amount)
        if amount < 0:
            if tags_ids['operating'] in tags_per_account.get(account_id, []):
                self._add_report_data('paid_operating_activities', aml_data, layout_data, report_data)
            elif tags_ids['operating_5'] in tags_per_account.get(account_id, []):
                self._add_report_data('paid_operating_5', aml_data, layout_data, report_data)
            elif tags_ids['operating_6'] in tags_per_account.get(account_id, []):
                self._add_report_data('paid_operating_6', aml_data, layout_data, report_data)
            elif tags_ids['operating_4'] in tags_per_account.get(account_id, []):
                self._add_report_data('paid_operating_4', aml_data, layout_data, report_data)
            else:
                self._add_report_data('unclassified_activities_cash_out', aml_data, layout_data, report_data)
        elif amount > 0:
            if tags_ids['operating_1'] in tags_per_account.get(account_id, []):
                self._add_report_data('received_operating_1', aml_data, layout_data, report_data)
            elif tags_ids['operating_2'] in tags_per_account.get(account_id, []):
                self._add_report_data('received_operating_2', aml_data, layout_data, report_data)
            elif tags_ids['operating'] in tags_per_account.get(account_id, []):
                self._add_report_data('received_operating_activities', aml_data, layout_data, report_data)
            elif tags_ids['operating_4'] in tags_per_account.get(account_id, []):
                self._add_report_data('received_operating_4', aml_data, layout_data, report_data)
            else:
                self._add_report_data('unclassified_activities_cash_in', aml_data, layout_data, report_data)

    def _get_layout_data(self):
        return {
            'opening_balance': {'name': '现金及现金等价物，期初', 'level': 0},
            'net_increase': {'name': '现金净增加额', 'level': 0},
                'operating_activities': {'name': '一、日常活动产生的现金流量', 'level': 2, 'parent_line_id': 'net_increase'},
                    'operating_activities_cash_in': {'name': '日常活动的现金流入', 'level': 3, 'parent_line_id': 'operating_activities'},
                        'received_operating_1': {'name': '财政基本支出拨款收到的现金', 'level': 5, 'parent_line_id': 'operating_activities_cash_in'},
                        'received_operating_2': {'name': '财政非资本性项目拨款收到的现金', 'level': 5, 'parent_line_id': 'operating_activities_cash_in'},
                        'received_operating_activities': {'name': '事业活动收到的除财政拨款以外的现金', 'level': 5, 'parent_line_id': 'operating_activities_cash_in'},
                        'received_operating_4': {'name': '收到的其他与日常活动有关的现金', 'level': 5, 'parent_line_id': 'operating_activities_cash_in'},
                    'operating_activities_cash_out': {'name': '日常活动的现金流出', 'level': 3, 'parent_line_id': 'operating_activities'},
                        'paid_operating_activities': {'name': '购买商品、接受劳务支付的现金', 'level': 5, 'parent_line_id': 'operating_activities_cash_out'},
                        'paid_operating_5': {'name': '支付给职工以及为职工支付的现金', 'level': 5, 'parent_line_id': 'operating_activities_cash_out'},
                        'paid_operating_6': {'name': '支付的各项税费', 'level': 5, 'parent_line_id': 'operating_activities_cash_out'},
                        'paid_operating_4': {'name': '支付的其他与日常活动有关的现金', 'level': 5, 'parent_line_id': 'operating_activities_cash_out'},
                'investing_activities': {'name': '二、投资活动产生的现金流量', 'level': 2, 'parent_line_id': 'net_increase'},
                    'investing_activities_cash_in': {'name': '投资活动的现金流入', 'level': 3, 'parent_line_id': 'investing_activities'},
                        'received_investing': {'name': '收回投资收到的现金', 'level': 5, 'parent_line_id': 'investing_activities_cash_in'},
                        'received_investing_1': {'name': '取得投资收益收到的现金', 'level': 5, 'parent_line_id': 'investing_activities_cash_in'},
                        'received_investing_2': {'name': '处置固定资产、无形资产、公共基础设施等收回的现金净额', 'level': 5, 'parent_line_id': 'investing_activities_cash_in'},
                        'received_investing_3': {'name': '收到的其他与投资活动有关的现金', 'level': 5, 'parent_line_id': 'investing_activities_cash_in'},
                    'investing_activities_cash_out': {'name': '投资活动的现金流出', 'level': 3, 'parent_line_id': 'investing_activities'},
                        'paid_investing_4': {'name': '购建固定资产、无形资产、公共基础设施等支付的现金', 'level': 5, 'parent_line_id': 'investing_activities_cash_out'},
                        'paid_investing_5': {'name': '支付给职工以及为职工支付的现金', 'level': 5, 'parent_line_id': 'investing_activities_cash_out'},
                        'paid_investing_6': {'name': '支付的各项税费', 'level': 5, 'parent_line_id': 'investing_activities_cash_out'},
                        'paid_investing_4': {'name': '支付的其他与日常活动有关的现金', 'level': 5, 'parent_line_id': 'investing_activities_cash_out'},
                'financing_activities': {'name': '三、筹资活动产生的现金流量', 'level': 2, 'parent_line_id': 'net_increase'},
                'unclassified_activities': {'name': '未分类活动产生的现金流量', 'level': 2, 'parent_line_id': 'net_increase'},
                    'unclassified_activities_cash_in': {'name': '现金流入', 'level': 3, 'parent_line_id': 'unclassified_activities'},
                    'unclassified_activities_cash_out': {'name': '现金流出', 'level': 3, 'parent_line_id': 'unclassified_activities'},
            'closing_balance': {'name': '现金及现金等价物，期末余额', 'level': 0},
        }

    def _get_layout_line(self, options, layout_line_id, layout_line_data, report_data):
        line_id = self._get_generic_line_id(None, None, markup=layout_line_id)
        unfold_all = self._context.get('print_mode') or options.get('unfold_all')
        unfoldable = 'aml_groupby_account' in report_data[layout_line_id] if layout_line_id in report_data else False

        value = report_data[layout_line_id].get('balance', 0.0) if layout_line_id in report_data else 0.0
        column_values = [{'name': value, 'class': 'number'}]

        return {
            'id': line_id,
            'name': layout_line_data['name'],
            'level': layout_line_data['level'],
            'class': 'o_account_reports_totals_below_sections' if self.env.company.totals_below_sections else '',
            'columns': column_values,
            'unfoldable': unfoldable,
            'unfolded': line_id in options['unfolded_lines'] or unfold_all,
        }

    def _get_aml_line(self, options, aml_data):
        parent_line_id = self._get_generic_line_id(None, None, aml_data['parent_line_id'])
        line_id = self._get_generic_line_id('account.account', aml_data['account_id'], parent_line_id=parent_line_id)

        value = aml_data['balance']
        column_values = [{'name': value, 'class': 'number'}]

        return {
            'id': line_id,
            'name': f"{aml_data['account_code']} {aml_data['account_name']}",
            'caret_options': 'account.account',
            'level': aml_data['level'],
            'parent_id': parent_line_id,
            'columns': column_values,
        }

    def _get_unexplained_difference_line(self, options, report_data):
        unexplained_difference = False

        opening_balance = report_data['opening_balance']['balance'] if 'opening_balance' in report_data else 0.0
        closing_balance = report_data['closing_balance']['balance'] if 'closing_balance' in report_data else 0.0
        net_increase = report_data['net_increase']['balance'] if 'net_increase' in report_data else 0.0

        delta = closing_balance - opening_balance - net_increase
        column_values = [{'name': delta, 'class': 'number'}]

        if unexplained_difference:
            return {
                'id': self._get_generic_line_id(None, None, markup='unexplained_difference'),
                'name': 'Unexplained Difference',
                'level': 0,
                'class': 'o_account_reports_totals_below_sections' if self.env.company.totals_below_sections else '',
                'columns': column_values,
            }
