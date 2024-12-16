# -*- coding: utf-8 -*-

from odoo import api, fields, models, Command, _, osv

class AccountAccountTemplate(models.Model):
    _inherit = "account.account.template"

    account_type = fields.Selection(
        selection_add=[
            ('budget_income', '预算收入'),
            ('budget_expense', '预算支出'),
            ('budget_surplus', '预算结余'),
        ],
        ondelete={
            'budget_income': lambda rec: rec.write({'account_type': 'off_balance'}),
            'budget_expense': lambda rec: rec.write({'account_type': 'off_balance'}),
            'budget_surplus': lambda rec: rec.write({'account_type': 'off_balance'}),
        },
    )
