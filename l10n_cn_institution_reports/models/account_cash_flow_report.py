# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class CashFlowReportCustomHandler(models.AbstractModel):
    _name = 'cn_institution.cash.flow.report.handler'
    _inherit = 'account.cash.flow.report.handler'
    _description = '现金流量表自定义处理程序'

    def _get_tags_ids(self):
        ''' Get a dict to pass on to _dispatch_aml_data containing information mapping account tags to report lines. '''
        return {
            'operating_1': self.env.ref('l10n_cn_institution.account_tag_operating_1').id,
            'operating_2': self.env.ref('l10n_cn_institution.account_tag_operating_2').id,
            'operating': self.env.ref('account.account_tag_operating').id,
            'operating_4': self.env.ref('l10n_cn_institution.account_tag_operating_4').id,
            'operating_5': self.env.ref('l10n_cn_institution.account_tag_operating_5').id,
            'operating_6': self.env.ref('l10n_cn_institution.account_tag_operating_6').id,
            'investing': self.env.ref('account.account_tag_investing').id,
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
