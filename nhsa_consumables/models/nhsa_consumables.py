# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class NHSAConsumables(models.Model):
    _name = "nhsa.consumables"
    _description = "医保医用耗材分类与代码"

    name = fields.Char('耗材代码', index='trigram', required=True)

    nhsa_consumables_categ_id = fields.Many2one(
        'nhsa.consumables.category', '耗材分类',
        required=True)
    nhsa_consumables_categ_code = fields.Char('分类码',
        related='nhsa_consumables_categ_id.code')

    common_name = fields.Char('通用名', required=True)
    material = fields.Char('材质', required=True)
    specifications = fields.Char('规格', required=True)
    enterprise = fields.Char('企业', required=True)

    product_count = fields.Integer(
        '# 产品', compute='_compute_product_count')
    supplier_count = fields.Integer(
        '# 供应', compute='_compute_supplier_count')

    def _compute_product_count(self):
        read_group_res = self.env['product.template'].read_group([('nhsa_consumables_id', 'in', self.ids)], ['nhsa_consumables_id'], ['nhsa_consumables_id'])
        group_data = dict((data['nhsa_consumables_id'][0], data['nhsa_consumables_id_count']) for data in read_group_res)
        for categ in self:
            product_count = 0
            for sub_categ_id in categ.search([('id', 'in', categ.ids)]).ids:
                product_count += group_data.get(sub_categ_id, 0)
            categ.product_count = product_count

    def _compute_supplier_count(self):
        read_group_res = self.env['product.supplierinfo'].read_group([('nhsa_consumables_id', 'in', self.ids)], ['nhsa_consumables_id'], ['nhsa_consumables_id'])
        group_data = dict((data['nhsa_consumables_id'][0], data['nhsa_consumables_id_count']) for data in read_group_res)
        for categ in self:
            supplier_count = 0
            for sub_categ_id in categ.search([('id', 'child_of', categ.ids)]).ids:
                supplier_count += group_data.get(sub_categ_id, 0)
            categ.supplier_count = supplier_count
