# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class GzMedicalConsumables(models.Model):
    _name = "gz.medical.consumables"
    _description = "贵州医保医用耗材目录"

    name = fields.Char('医用耗材代码', index='trigram', required=True)
    primary_classification = fields.Char('一级分类', required=True)
    secondary_classification = fields.Char('二级分类', required=True)
    tertiary_classification = fields.Char('三级分类', required=True)
    common_name = fields.Char('医保通用名', required=True)
    material = fields.Char('材质', required=True)
    characteristics = fields.Char('特性', required=True)
    payment_category = fields.Char('支付类别', required=True)
    payment_standard = fields.Float('支付标准', required=True)
    description = fields.Text('备注')

    nhsa_consumables_categ_id = fields.Many2one(
        'nhsa.consumables.category', '耗材分类',
        compute='_compute_nhsa_consumables_categ_id', store=True)
    
    @api.depends('name')
    def _compute_nhsa_consumables_categ_id(self):
        for record in self:
            nhsa_categ = self.env['nhsa.consumables.category'].search([
                ('code', '=', record.name[:7])
            ], limit=1)
            record.nhsa_consumables_categ_id = nhsa_categ.id if nhsa_categ else False
