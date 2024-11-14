# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, _
from odoo.addons.account.models.chart_template import template

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @template('cn_institution')
    def _get_cn_institution_template_data(self):
        return {
            'name': '行政事业单位',
            'code_digits': 6,
            'use_storno_accounting': True,
            'property_account_receivable_id': 'account_template_1212',
            'property_account_payable_id': 'account_template_2302',
            'property_account_expense_categ_id': 'account_template_5001',
            'property_account_income_categ_id': 'account_template_4101',
        }

    @template('cn_institution', 'res.company')
    def _get_cn_institution_res_company(self):
        return {
            self.env.company.id: {
                'account_fiscal_country_id': 'base.cn',
                'bank_account_code_prefix': '1002',
                'cash_account_code_prefix': '1001',
                'transfer_account_code_prefix': '1012',
                'account_default_pos_receivable_account_id': 'account_template_1212',
                'income_currency_exchange_account_id': 'account_template_4609',
                'expense_currency_exchange_account_id': 'account_template_5101',
                'account_price_include': 'tax_included',
                'account_sale_tax_id': 'tax_sales_excluded_13',
                'account_purchase_tax_id': 'tax_purchase_excluded_13',
                'account_journal_suspense_account_id': 'account_template_100207',
                'default_cash_difference_income_account_id': 'account_template_1902',
                'default_cash_difference_expense_account_id': 'account_template_1902',
            },
        }

    @template('cn_institution', 'account.journal')
    def _get_cn_institution_account_journal(self):
        return {
            'cash': {
                'name': '库存现金',
                'default_account_id': 'account_template_1001',
            },
            'bank': {
                'default_account_id': 'account_template_100201',
            },
        }
