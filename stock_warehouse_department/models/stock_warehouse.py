# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, _lt, api, fields, models

class Warehouse(models.Model):
    _inherit = "stock.warehouse"

    responsible_id = fields.Many2one(
        'res.users', string='负责人', company_dependent=True, check_company=True)
    department_id = fields.Many2one('hr.department', '部门', compute='_compute_department_id', store=True, readonly=False)

    @api.depends('responsible_id')
    def _compute_department_id(self):
        for record in self:
            record.department_id = self.responsible_id.department_id.id if self.responsible_id else False
