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
            'investing': self.env.ref('account.account_tag_investing').id,
            'financing': self.env.ref('account.account_tag_financing').id,
        }

    def _dispatch_aml_data(self, tags_ids, aml_data, layout_data, report_data):
        if aml_data['balance'] < 0:
            if aml_data['account_tag_id'] == tags_ids['operating_4001']:
                self._add_report_data('received_operating_4001', aml_data, layout_data, report_data)
        elif aml_data['balance'] > 0:
            d = 0

    def _get_layout_data(self):
        return {
            'net_increase': {'name': '现金净增加额', 'level': 0},
                'operating_activities': {'name': '日常活动产生的现金流量', 'level': 2, 'parent_line_id': 'net_increase'},
                    'received_operating_4001': {'name': '财政基本支出拨款收到的现金', 'level': 3, 'parent_line_id': 'operating_activities'},
        }