# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    def name_get(self):
        res = []
        for analytic in self:
            name = analytic.complete_name
            if analytic.code:
                name = ("%(plan_name)s [%(code)s] %(name)s") % {"plan_name": analytic.plan_id.name, "code": analytic.code, "name": name}
            else:
                name = ("%(plan_name)s %(name)s") % {"plan_name": analytic.plan_id.name, "name": name}
            if analytic.partner_id:
                name = _("%(name)s - %(partner)s") % {
                    "name": name,
                    "partner": analytic.partner_id.commercial_partner_id.name,
                }
            res.append((analytic.id, name))
        return res
