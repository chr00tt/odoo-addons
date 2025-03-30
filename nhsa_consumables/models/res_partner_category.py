# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api,  models
from odoo.exceptions import UserError

class PartnerCategory(models.Model):
    _inherit = "res.partner.category"

    @api.ondelete(at_uninstall=False)
    def _unlink_except_default_category(self):
        patient_category = self.env.ref('nhsa_consumables.res_partner_category_manufacturer', raise_if_not_found=False)
        if patient_category and patient_category in self:
            raise UserError(_("不能删除 %s 标签！", patient_category.name))
