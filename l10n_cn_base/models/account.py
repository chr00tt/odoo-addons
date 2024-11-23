# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountAccountType(models.Model):
    _inherit = "account.account.type"

    internal_group = fields.Selection(selection_add=[('off_balance', '表外科目')])
