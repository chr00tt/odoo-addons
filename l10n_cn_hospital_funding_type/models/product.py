# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_stock_valuation_account1_id = fields.Many2one(
        'account.account', '库存计价科目(财政项目拨款经费)', company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0]), ('deprecated', '=', False)]", check_company=True)
    property_stock_valuation_account2_id = fields.Many2one(
        'account.account', '库存计价科目(科教经费)', company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0]), ('deprecated', '=', False)]", check_company=True)

    @api.onchange('property_stock_valuation_account_id')
    def onchange_property_stock_valuation_account_id(self):
        if self.property_stock_valuation_account_id:
            if not self.property_stock_valuation_account1_id:
                self.property_stock_valuation_account1_id = self.property_stock_valuation_account_id
            if not self.property_stock_valuation_account2_id:
                self.property_stock_valuation_account2_id = self.property_stock_valuation_account_id
