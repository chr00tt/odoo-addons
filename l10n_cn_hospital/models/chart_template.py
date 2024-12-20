# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, _

class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    def _load(self, company):
        res = super()._load(company)

        if self == self.env.ref("l10n_cn_hospital.chart_template_hospital"):
            self._load_product_category(company)

        return res

    def _load_product_category(self, company):
        #self.env.ref("l10n_cn_hospital.product_category_1").with_company(company).
        d = 1