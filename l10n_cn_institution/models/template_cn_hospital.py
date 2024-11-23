# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, _
from odoo.addons.account.models.chart_template import template

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @template('cn_hospital')
    def _get_cn_hospital_template_data(self):
        return {
            'name': '医院',
            'parent': 'cn_institution',
            'property_account_receivable_id': 'account_template_hospital_121203',
            'property_stock_valuation_account_id': 'account_template_hospital_130201',
            'property_tax_payable_account_id': 'account_template_hospital_21010105',
            'property_tax_receivable_account_id': 'account_template_hospital_21010101',
        }

    @template('cn_hospital', 'res.company')
    def _get_cn_hospital_res_company(self):
        res = super()._get_cn_institution_res_company()
        res[self.env.company.id].update({
            'account_default_pos_receivable_account_id': 'account_template_hospital_121203',
        })
        return res
