# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    def name_get(self):
        res = []
        for analytic in self:
            name = analytic.name
            plan_name = analytic.plan_id.name
            if analytic.code:
                name = f'{plan_name} [{analytic.code}] {name}'
            if analytic.partner_id.commercial_partner_id.name:
                name = f'{plan_name} {name} - {analytic.partner_id.commercial_partner_id.name}'
            res.append((analytic.id, name))
        return res
