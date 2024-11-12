# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, Command

class AccountMove(models.Model):
    _inherit = "account.move"

    funding_type = fields.Selection(
        selection=[
            ('1', '财政项目拨款经费'),
            ('2', '科教经费'),
            ('3', '其他经费'),
        ],
        string='经费性质',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        tracking=True,
        default='3',
    )
