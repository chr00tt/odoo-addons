# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools

class AccountAccount(models.Model):
    _inherit = "account.account"

    #通过设置默认值的方法不支持根据其他字段的值动态设置默认值，故使用compute 
    balance_direction = fields.Selection(
        selection=[
            ('1', '借'),
            ('-1', '贷'),
        ],
        string='余额方向', required=True,store=True,compute='_compute_balance_direction', precompute=True)

    @api.depends('code')
    def _compute_balance_direction(self):
        account_direction = [
            {'min': 0, 'max': 1219, 'id': '1'},
            {'min': 1219, 'max': 1220, 'id': '-1'},
            {'min': 1220, 'max': 1602, 'id': '1'},
            {'min': 1602, 'max': 1610, 'id': '-1'},
            {'min': 1610, 'max': 1702, 'id': '1'},
            {'min': 1702, 'max': 1710, 'id': '-1'},
            {'min': 1710, 'max': 2000, 'id': '1'},
            {'min': 2000, 'max': 5000, 'id': '-1'},
            {'min': 5000, 'max': 6000, 'id': '1'},
            {'min': 6000, 'max': 7000, 'id': '-1'},
            {'min': 7000, 'max': 8000, 'id': '1'},
            {'min': 8000, 'max': 9000, 'id': '-1'},
        ]
        for record in self:
            if not record.balance_direction:
                if record.code:
                    code = int(record.code[:4])
                    if code >= 9000:
                        if record.account_type == "income_other":
                            record.balance_direction = "-1"
                        elif record.account_type == "expense":
                            record.balance_direction = "1"
                        elif record.account_type == "equity_unaffected":
                            record.balance_direction = "-1"
                        else:
                            record.balance_direction = "1"
                    else:
                        for direction in account_direction:
                            if code in range(direction['min'], direction['max']):
                                record.balance_direction = direction['id']
                else:
                    record.balance_direction = "1"
