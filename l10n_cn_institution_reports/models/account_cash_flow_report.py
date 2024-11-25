# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountCashFlowReport(models.AbstractModel):
    _name = 'cn_institution.cash.flow.report'
    _inherit = 'account.cash.flow.report'
    _description = '现金流量表'

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

    def _dispatch_aml_data(self, tags_ids, aml_data, layout_data, report_data):
        if aml_data['balance'] < 0:
            if aml_data['account_tag_id'] == tags_ids['operating']:
                self._add_report_data('paid_operating_activities', aml_data, layout_data, report_data)
            elif aml_data['account_tag_id'] == tags_ids['operating_5']:
                self._add_report_data('paid_operating_5', aml_data, layout_data, report_data)
            elif aml_data['account_tag_id'] == tags_ids['operating_6']:
                self._add_report_data('paid_operating_6', aml_data, layout_data, report_data)
            elif aml_data['account_tag_id'] == tags_ids['operating_4']:
                self._add_report_data('paid_operating_4', aml_data, layout_data, report_data)
            else:
                self._add_report_data('unclassified_activities_cash_out', aml_data, layout_data, report_data)
        elif aml_data['balance'] > 0:
            if aml_data['account_tag_id'] == tags_ids['operating_1']:
                self._add_report_data('received_operating_1', aml_data, layout_data, report_data)
            elif aml_data['account_tag_id'] == tags_ids['operating_2']:
                self._add_report_data('received_operating_2', aml_data, layout_data, report_data)
            elif aml_data['account_tag_id'] == tags_ids['operating']:
                self._add_report_data('received_operating_activities', aml_data, layout_data, report_data)
            elif aml_data['account_tag_id'] == tags_ids['operating_4']:
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

    @api.model
    def _get_lines(self, options, line_id=None):

        def _insert_at_index(index, account_id, account_code, account_name, amount):
            ''' Insert the amount in the right section depending the line's index and the account_id. '''
            # Helper used to add some values to the report line having the index passed as parameter
            # (see _get_lines_to_compute).
            line = lines_to_compute[index]

            if self.env.company.currency_id.is_zero(amount):
                return

            line.setdefault('unfolded_lines', {})
            line['unfolded_lines'].setdefault(account_id, {
                'id': account_id,
                'name': '%s %s' % (account_code, account_name),
                'level': line['level'] + 1,
                'parent_id': line['id'],
                'columns': [{'name': 0.0, 'class': 'number'}],
            })
            line['columns'][0]['name'] += amount
            line['unfolded_lines'][account_id]['columns'][0]['name'] += amount

        def _dispatch_result(account_id, account_code, account_name, account_internal_type, amount):
            ''' Dispatch the newly fetched line inside the right section. '''
            if account_internal_type == 'receivable':
                # 'Advance Payments received from customers'                (index=3)
                _insert_at_index(3, account_id, account_code, account_name, -amount)
            elif account_internal_type == 'payable':
                # 'Advance Payments made to suppliers'                      (index=5)
                _insert_at_index(5, account_id, account_code, account_name, -amount)
            elif amount < 0:
                if tag_operating_id in tags_per_account.get(account_id, []):
                    # 'Cash received from operating activities'             (index=4)
                    _insert_at_index(4, account_id, account_code, account_name, -amount)
                elif tag_investing_id in tags_per_account.get(account_id, []):
                    # 'Cash in for investing activities'                    (index=8)
                    _insert_at_index(8, account_id, account_code, account_name, -amount)
                elif tag_financing_id in tags_per_account.get(account_id, []):
                    # 'Cash in for financing activities'                    (index=11)
                    _insert_at_index(11, account_id, account_code, account_name, -amount)
                else:
                    # 'Cash in for unclassified activities'                 (index=14)
                    _insert_at_index(14, account_id, account_code, account_name, -amount)
            elif amount > 0:
                if tag_operating_id in tags_per_account.get(account_id, []):
                    # 'Cash paid for operating activities'                  (index=6)
                    _insert_at_index(6, account_id, account_code, account_name, -amount)
                elif tag_investing_id in tags_per_account.get(account_id, []):
                    # 'Cash out for investing activities'                   (index=9)
                    _insert_at_index(9, account_id, account_code, account_name, -amount)
                elif tag_financing_id in tags_per_account.get(account_id, []):
                    # 'Cash out for financing activities'                   (index=12)
                    _insert_at_index(12, account_id, account_code, account_name, -amount)
                else:
                    # 'Cash out for unclassified activities'                (index=15)
                    _insert_at_index(15, account_id, account_code, account_name, -amount)

        self.flush()

        unfold_all = self._context.get('print_mode') or options.get('unfold_all')
        currency_table_query = self.env['res.currency']._get_query_currency_table(options)
        lines_to_compute = self._get_lines_to_compute(options)

        tag_operating_id = self.env.ref('account.account_tag_operating').id
        tag_investing_id = self.env.ref('account.account_tag_investing').id
        tag_financing_id = self.env.ref('account.account_tag_financing').id
        tag_ids = (tag_operating_id, tag_investing_id, tag_financing_id)
        tags_per_account = self._get_tags_per_account(options, tag_ids)

        payment_move_ids, payment_account_ids = self._get_liquidity_move_ids(options)

        # Compute 'Cash and cash equivalents, beginning of period'      (index=0)
        beginning_period_options = self._get_options_beginning_period(options)
        for account_id, account_code, account_name, balance in self._compute_liquidity_balance(beginning_period_options, currency_table_query, payment_account_ids):
            _insert_at_index(0, account_id, account_code, account_name, balance)
            _insert_at_index(16, account_id, account_code, account_name, balance)

        # Compute 'Cash and cash equivalents, closing balance'          (index=16)
        for account_id, account_code, account_name, balance in self._compute_liquidity_balance(options, currency_table_query, payment_account_ids):
            _insert_at_index(16, account_id, account_code, account_name, balance)

        # ==== Process liquidity moves ====
        res = self._get_liquidity_move_report_lines(options, currency_table_query, payment_move_ids, payment_account_ids)
        for account_id, account_code, account_name, account_internal_type, amount in res:
            _dispatch_result(account_id, account_code, account_name, account_internal_type, amount)

        # ==== Process reconciled moves ====
        res = self._get_reconciled_move_report_lines(options, currency_table_query, payment_move_ids, payment_account_ids)
        for account_id, account_code, account_name, account_internal_type, balance in res:
            _dispatch_result(account_id, account_code, account_name, account_internal_type, balance)

        # 'Cash flows from operating activities'                            (index=2)
        lines_to_compute[2]['columns'][0]['name'] = \
            lines_to_compute[3]['columns'][0]['name'] + \
            lines_to_compute[4]['columns'][0]['name'] + \
            lines_to_compute[5]['columns'][0]['name'] + \
            lines_to_compute[6]['columns'][0]['name']
        # 'Cash flows from investing & extraordinary activities'            (index=7)
        lines_to_compute[7]['columns'][0]['name'] = \
            lines_to_compute[8]['columns'][0]['name'] + \
            lines_to_compute[9]['columns'][0]['name']
        # 'Cash flows from financing activities'                            (index=10)
        lines_to_compute[10]['columns'][0]['name'] = \
            lines_to_compute[11]['columns'][0]['name'] + \
            lines_to_compute[12]['columns'][0]['name']
        # 'Cash flows from unclassified activities'                         (index=13)
        lines_to_compute[13]['columns'][0]['name'] = \
            lines_to_compute[14]['columns'][0]['name'] + \
            lines_to_compute[15]['columns'][0]['name']
        # 'Net increase in cash and cash equivalents'                       (index=1)
        lines_to_compute[1]['columns'][0]['name'] = \
            lines_to_compute[2]['columns'][0]['name'] + \
            lines_to_compute[7]['columns'][0]['name'] + \
            lines_to_compute[10]['columns'][0]['name'] + \
            lines_to_compute[13]['columns'][0]['name']

        # ==== Compute the unexplained difference ====

        closing_ending_gap = lines_to_compute[16]['columns'][0]['name'] - lines_to_compute[0]['columns'][0]['name']
        computed_gap = sum(lines_to_compute[index]['columns'][0]['name'] for index in [2, 7, 10, 13])
        delta = closing_ending_gap - computed_gap
        if not self.env.company.currency_id.is_zero(delta):
            lines_to_compute.insert(16, {
                'id': 'cash_flow_line_unexplained_difference',
                'name': _('Unexplained Difference'),
                'level': 0,
                'columns': [{'name': delta, 'class': 'number'}],
            })

        # ==== Build final lines ====

        lines = []
        for line in lines_to_compute:
            unfolded_lines = line.pop('unfolded_lines', {})
            sub_lines = [unfolded_lines[k] for k in sorted(unfolded_lines)]

            line['unfoldable'] = len(sub_lines) > 0
            line['unfolded'] = line['unfoldable'] and (unfold_all or line['id'] in options['unfolded_lines'])

            # Header line.
            line['columns'][0]['name'] = self.format_value(line['columns'][0]['name'])
            lines.append(line)

            # Sub lines.
            for sub_line in sub_lines:
                sub_line['columns'][0]['name'] = self.format_value(sub_line['columns'][0]['name'])
                sub_line['style'] = '' if line['unfolded'] else 'display: none;'
                lines.append(sub_line)

            # Total line.
            if line['unfoldable']:
                lines.append({
                    'id': '%s_total' % line['id'],
                    'name': _('Total') + ' ' + line['name'],
                    'level': line['level'] + 1,
                    'parent_id': line['id'],
                    'columns': line['columns'],
                    'class': 'o_account_reports_domain_total',
                    'style': '' if line['unfolded'] else 'display: none;',
                })
        return lines

    @api.model
    def _get_report_name(self):
        return '现金流量表（行政事业单位）'
