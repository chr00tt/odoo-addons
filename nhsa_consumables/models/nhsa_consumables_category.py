# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class NHSAConsumablesCategory(models.Model):
    _name = "nhsa.consumables.category"
    _description = "医保医用耗材分类"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'code'

    name = fields.Char('名称', index='trigram', required=True)
    complete_name = fields.Char(
        '完整名称', compute='_compute_complete_name', recursive=True,
        store=True)
    parent_id = fields.Many2one('nhsa.consumables.category', '上级分类', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True, unaccent=False)
    child_id = fields.One2many('nhsa.consumables.category', 'parent_id', '下级分类')
    nhsa_consumables_count = fields.Integer(
        '# 耗材', compute='_compute_nhsa_consumables_count')
    product_count = fields.Integer(
        '# 产品', compute='_compute_product_count')
    supplier_count = fields.Integer(
        '# 供应', compute='_compute_supplier_count')

    code = fields.Char('编号', default="/", index=True)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    def _compute_nhsa_consumables_count(self):
        read_group_res = self.env['nhsa.consumables'].read_group([('nhsa_consumables_categ_id', 'child_of', self.ids)], ['nhsa_consumables_categ_id'], ['nhsa_consumables_categ_id'])
        group_data = dict((data['nhsa_consumables_categ_id'][0], data['nhsa_consumables_categ_id_count']) for data in read_group_res)
        for categ in self:
            nhsa_consumables_count = 0
            for sub_categ_id in categ.search([('id', 'child_of', categ.ids)]).ids:
                nhsa_consumables_count += group_data.get(sub_categ_id, 0)
            categ.nhsa_consumables_count = nhsa_consumables_count

    def _compute_product_count(self):
        read_group_res = self.env['product.template'].read_group([('nhsa_consumables_categ_id', 'child_of', self.ids)], ['nhsa_consumables_categ_id'], ['nhsa_consumables_categ_id'])
        group_data = dict((data['nhsa_consumables_categ_id'][0], data['nhsa_consumables_categ_id_count']) for data in read_group_res)
        for categ in self:
            product_count = 0
            for sub_categ_id in categ.search([('id', 'child_of', categ.ids)]).ids:
                product_count += group_data.get(sub_categ_id, 0)
            categ.product_count = product_count

    def _compute_supplier_count(self):
        read_group_res = self.env['product.supplierinfo'].read_group([('categ_id', 'child_of', self.ids)], ['categ_id'], ['categ_id'])
        group_data = dict((data['categ_id'][0], data['categ_id_count']) for data in read_group_res)
        for categ in self:
            supplier_count = 0
            for sub_categ_id in categ.search([('id', 'child_of', categ.ids)]).ids:
                supplier_count += group_data.get(sub_categ_id, 0)
            categ.supplier_count = supplier_count

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError('不能创建递归的类别.')

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]

    def name_get(self):
        if not self.env.context.get('hierarchical_naming', True):
            return [(record.id, record.name) for record in self]
        return super().name_get()

    @api.ondelete(at_uninstall=False)
    def _unlink_except_default_category(self):
        main_category = self.env.ref('nhsa_consumables.nhsa_consumables_category_all', raise_if_not_found=False)
        if main_category and main_category in self:
            raise UserError("不能删除此耗材类别，它是默认的常规类别。")
