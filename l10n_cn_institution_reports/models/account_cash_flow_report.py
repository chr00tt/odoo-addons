# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class CashFlowReportCustomHandler(models.AbstractModel):
    _name = 'cn_institution.cash.flow.report.handler'
    _inherit = 'account.cash.flow.report.handler'
    _description = '现金流量表自定义处理程序'

    def _get_tags_ids(self):
        ''' Get a dict to pass on to _dispatch_aml_data containing information mapping account tags to report lines. '''
        return {
            'operating_4001': self.env.ref('l10n_cn_institution.account_tag_operating_4001').id,
            'operating': self.env.ref('l10n_cn_institution.account_tag_operating').id,
            'investing': self.env.ref('account.account_tag_investing').id,
            'financing': self.env.ref('account.account_tag_financing').id,
        }

    def _dispatch_aml_data(self, tags_ids, aml_data, layout_data, report_data):
        if aml_data['balance'] < 0:
            if aml_data['account_tag_id'] == tags_ids['operating_4001']:
                self._add_report_data('received_operating_4001', aml_data, layout_data, report_data)
            elif aml_data['account_tag_id'] == tags_ids['operating']:
                self._add_report_data('paid_operating_activities', aml_data, layout_data, report_data)
            else:
                self._add_report_data('unclassified_activities_cash_out', aml_data, layout_data, report_data)
        elif aml_data['balance'] > 0:
            if aml_data['account_tag_id'] == tags_ids['operating']:
                self._add_report_data('received_operating_activities', aml_data, layout_data, report_data)
            else:
                self._add_report_data('unclassified_activities_cash_in', aml_data, layout_data, report_data)

    def _get_layout_data(self):
        return {
            'opening_balance': {'name': '现金及现金等价物，期初', 'level': 0},
            'net_increase': {'name': '现金净增加额', 'level': 0},
                'operating_activities': {'name': '一、日常活动产生的现金流量', 'level': 2, 'parent_line_id': 'net_increase'},
                    'operating_activities_cash_in': {'name': '日常活动的现金流入', 'level': 3, 'parent_line_id': 'operating_activities'},
                        'received_operating_4001': {'name': '财政基本支出拨款收到的现金', 'level': 5, 'parent_line_id': 'operating_activities_cash_in'},
                        'received_operating_activities': {'name': '事业活动收到的除财政拨款以外的现金', 'level': 5, 'parent_line_id': 'operating_activities_cash_in'},
                    'operating_activities_cash_out': {'name': '日常活动的现金流出', 'level': 3, 'parent_line_id': 'operating_activities'},
                        'paid_operating_activities': {'name': '购买商品、接受劳务支付的现金', 'level': 5, 'parent_line_id': 'operating_activities_cash_out'},
                'investing_activities': {'name': '二、投资活动产生的现金流量', 'level': 2, 'parent_line_id': 'net_increase'},
                'financing_activities': {'name': '三、筹资活动产生的现金流量', 'level': 2, 'parent_line_id': 'net_increase'},
                'unclassified_activities': {'name': '未分类活动产生的现金流量', 'level': 2, 'parent_line_id': 'net_increase'},
                    'unclassified_activities_cash_in': {'name': '现金流入', 'level': 3, 'parent_line_id': 'unclassified_activities'},
                    'unclassified_activities_cash_out': {'name': '现金流出', 'level': 3, 'parent_line_id': 'unclassified_activities'},
            'closing_balance': {'name': '现金及现金等价物，期末余额', 'level': 0},
        }
