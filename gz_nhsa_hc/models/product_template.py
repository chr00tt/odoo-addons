# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    gz_nhsa_consumables_id = fields.Many2one('gz.medical.consumables', '贵州医保目录', compute='_compute_gz_nhsa_consumables_id', store=True)

    @api.depends('ybbm')
    def _compute_gz_nhsa_consumables_id(self):
        for template in self:
            if template.ybbm:
                ybbm = template.ybbm[:15]
                gz_nhsa_consumables = self.env['gz.medical.consumables'].search([('name', '=', ybbm)], limit=1)
                if gz_nhsa_consumables:
                    template.gz_nhsa_consumables_id = gz_nhsa_consumables
                else:
                    template.gz_nhsa_consumables_id = False
            else:
                template.gz_nhsa_consumables_id = False
