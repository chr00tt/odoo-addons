# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    def _load(self, company):
        res = super(AccountChartTemplate, self)._load(company)
        if self == self.env.ref('l10n_cn_hospital.chart_template_hospital'):
            self._load_product_category(company)
        return res

    def _load_product_category(self, company):
        AccountAccount = self.env['account.account']
        categories = [
            {'id': 'l10n_cn_hospital_asset.product_category_01', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0101', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0102', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0103', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0104', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0105', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0106', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0107', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0108', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0109', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0110', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0111', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0112', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_02', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0201', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0202', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0203', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0204', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0205', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0206', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0207', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0208', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0209', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0210', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0211', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0212', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0213', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0214', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0215', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0216', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0217', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0218', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0219', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_03', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0301', 'account_id': '1601'},
            {'id': 'l10n_cn_hospital_asset.product_category_0302', 'account_id': '1601'},
        ]
        for category in categories:
            self.env.ref(category['id']).with_company(company).write({
                'property_valuation': 'real_time',
                'property_stock_valuation_account_id': AccountAccount.search([('code', '=', category['account_id']), ('company_id', '=', company.id)], limit=1),
            })
