# -*- coding: utf-8 -*-

from odoo import api, fields, models, Command, _, osv

class AccountChartTemplate(models.Model):
    _inherit= "account.chart.template"

    @api.model
    def generate_journals(self, acc_template_ref, company, journals_dict=None):
        journal_to_add = (journals_dict or []) + [{'name': '收支结转', 'type': 'general', 'code': 'SZJZ', 'favorite': False, 'sequence': 8}]
        return super(AccountChartTemplate, self).generate_journals(acc_template_ref=acc_template_ref, company=company, journals_dict=journal_to_add)
