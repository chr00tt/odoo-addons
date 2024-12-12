# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_analytic_account_name = fields.Boolean('分析科目显示计划名称')
