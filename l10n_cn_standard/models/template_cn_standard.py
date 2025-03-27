from odoo import models
from odoo.addons.account.models.chart_template import template

class AccountChartTemplate(models.AbstractModel):
    _inherit = "account.chart.template"

    @template('cn_standard')
    def _get_cn_standard_template_data(self):
        """Return the data necessary for the chart template.

        :return: all the values that are not stored but are used to instancieate
                 the chart of accounts. Common keys are:
                 * property_*
                 * code_digits
        :rtype: dict
        """
        return {
            'name': '企业会计准则',
            'code_digits': '6',
            'property_account_receivable_id': 'account_1122',
            'property_account_payable_id': 'account_2202',
            'property_account_expense_categ_id': 'account_6401',
            'property_account_income_categ_id': 'account_6001',
            'property_stock_account_input_categ_id': 'account_1402',
            'property_stock_account_output_categ_id': 'account_1406',
            'property_stock_valuation_account_id': 'account_1405',
            # 'property_stock_account_production_cost_id': 'cost_of_production',
        }

    @template('cn_standard', 'res.company')
    def _get_cn_standard_res_company(self):
        """Return the data to be written on the company.

        The data is a mapping the XMLID to the create/write values of a record.

        :rtype: dict[(str, int), dict]
        """
        return {
            self.env.company.id: {
                'anglo_saxon_accounting': True,
                'account_fiscal_country_id': 'base.cn',
                'bank_account_code_prefix': '1002',
                'cash_account_code_prefix': '1001',
                'transfer_account_code_prefix': '1012',
                'account_default_pos_receivable_account_id': 'account_1124',
                'income_currency_exchange_account_id': 'account_6061',
                'expense_currency_exchange_account_id': 'account_6711',
                # 'default_cash_difference_income_account_id': 'cash_diff_income',
                # 'default_cash_difference_expense_account_id': 'cash_diff_expense',
                # 'account_journal_early_pay_discount_loss_account_id': 'cash_discount_loss',
                # 'account_journal_early_pay_discount_gain_account_id': 'cash_discount_gain',
                'account_sale_tax_id': 'account_tax_sales_included_13',
                'account_purchase_tax_id': 'account_tax_purchase_excluded_13',
            }
        }
