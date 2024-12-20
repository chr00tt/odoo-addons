# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    def _load(self, company):
        res = super(AccountChartTemplate, self)._load(company)
        if self == self.env.ref('l10n_cn_hospital.chart_template_hospital'):
            self._create_account_asset(company)

            self.env['account.account'].search([('code', '=', '1601'), ('company_id', '=', company.id)]).write({
                'create_asset': 'draft',
                'multiple_assets_per_line': True,
            })
        return res

    def _create_account_asset(self, company):
        # 财会〔2018〕24号 关于医院执行《政府会计制度——行政事业单位会计科目和报表》的补充规定.
        model_data = [
            {'name': '钢结构业务及管理用房', 'method_number': 50*12},
            {'name': '钢筋混凝土结构构业务及管理用房', 'method_number': 50*12},
            {'name': '砖混结构业务及管理用房', 'method_number': 30*12},
            {'name': '砖木结构业务及管理用房', 'method_number': 30*12},
            {'name': '简易房', 'method_number': 8*12},
            {'name': '房屋附属设施', 'method_number': 8*12},
            {'name': '构筑物', 'method_number': 8*12},
            {'name': '计算机设备', 'method_number': 6*12},
            {'name': '通信设备', 'method_number': 5*12},
            {'name': '办公设备', 'method_number': 6*12},
            {'name': '车辆', 'method_number': 10*12},
            {'name': '图书档案设备', 'method_number': 5*12},
            {'name': '机械设备', 'method_number': 10*12},
            {'name': '电气设备', 'method_number': 5*12},
            {'name': '雷达、无线电和卫星导航设备', 'method_number': 10*12},
            {'name': '广播、电视、电影设备', 'method_number': 5*12},
            {'name': '仪器仪表', 'method_number': 5*12},
            {'name': '电子和通信测量设备', 'method_number': 5*12},
            {'name': '计量标准器具及量具、衡器', 'method_number': 5*12},
            {'name': '医用电子仪器', 'method_number': 5*12},
            {'name': '医用超声仪器', 'method_number': 6*12},
            {'name': '医用高频仪器设备', 'method_number': 5*12},
            {'name': '物理治疗及体疗设备', 'method_number': 5*12},
            {'name': '高压氧舱', 'method_number': 6*12},
            {'name': '中医仪器设备', 'method_number': 5*12},
            {'name': '医用磁共振设备', 'method_number': 6*12},
            {'name': '医用X线设备', 'method_number': 6*12},
            {'name': '高能射线设备', 'method_number': 8*12},
            {'name': '医用核素设备', 'method_number': 6*12},
            {'name': '临床检验分析仪器', 'method_number': 5*12},
            {'name': '体外循环设备', 'method_number': 5*12},
            {'name': '手术急救设备', 'method_number': 5*12},
            {'name': '口腔设备', 'method_number': 6*12},
            {'name': '病房护理设备', 'method_number': 5*12},
            {'name': '消毒设备', 'method_number': 6*12},
            {'name': '其他专用设备', 'method_number': 5*12},
            {'name': '光学仪器及窥镜', 'method_number': 6*12},
            {'name': '激光仪器设备', 'method_number': 5*12},
            {'name': '家具', 'method_number': 15*12},
            {'name': '用具、装具', 'method_number': 5*12},
        ]

        AccountAccount = self.env['account.account']
        account_data = {
            'account_asset_id': AccountAccount.search([('code', '=', '1601'), ('company_id', '=', company.id)], limit=1).id,
            'account_depreciation_id': AccountAccount.search([('code', '=', '1602'), ('company_id', '=', company.id)], limit=1).id,
            'account_depreciation_expense_id': AccountAccount.search([('code', '=', '5001'), ('company_id', '=', company.id)], limit=1).id,
        }

        journal = self.env['account.journal'].search([('type', '=', 'general')], limit=1)

        asset_model_data_list = []
        for data in model_data:
            data.update({
                'method': 'linear',
                'method_period': '1',
                'company_id': company.id,
                'journal_id': journal.id,
                'state': 'model',
                'asset_type': 'purchase',
            })
            data.update(account_data)
            asset_model_data_list.append(data)
        self.env['account.asset'].create(asset_model_data_list)
