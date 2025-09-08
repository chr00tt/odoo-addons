# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class MedicalDeficeCategory(models.Model):
    _name = "medical.device.category"
    _description = "医疗器械分类"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char('名称', index='trigram', required=True)
    complete_name = fields.Char(
        '完整名称', compute='_compute_complete_name', recursive=True,
        store=True)
    parent_id = fields.Many2one('medical.device.category', '上级分类', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True, unaccent=False)
    child_id = fields.One2many('medical.device.category', 'parent_id', '下级分类')
    udi_data_count = fields.Integer(
        '# 唯一标识', compute='_compute_udi_data_count')
    product_count = fields.Integer(
        '# 产品', compute='_compute_product_count')
    supplier_count = fields.Integer(
        '# 供应', compute='_compute_supplier_count')

    code = fields.Char('编号', default="/", index=True)

    cpms = fields.Char('产品描述')
    yqyt = fields.Char('预期用途')
    pmjl = fields.Char('品名举例')
    gllb = fields.Selection([('1', 'Ⅰ'), ('2', 'Ⅱ'), ('3', 'Ⅲ')], string='管理类别')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    def _compute_udi_data_count(self):
        read_group_res = self.env['udi.data'].read_group([('flbm', 'child_of', self.ids)], ['flbm'], ['flbm'])
        group_data = dict((data['flbm'][0], data['flbm_count']) for data in read_group_res)
        for categ in self:
            udi_data_count = 0
            for sub_categ_id in categ.search([('id', 'child_of', categ.ids)]).ids:
                udi_data_count += group_data.get(sub_categ_id, 0)
            categ.udi_data_count = udi_data_count

    def _compute_product_count(self):
        read_group_res = self.env['product.template'].read_group([('udi_flbm', 'child_of', self.ids)], ['udi_flbm'], ['udi_flbm'])
        group_data = dict((data['udi_flbm'][0], data['udi_flbm_count']) for data in read_group_res)
        for categ in self:
            product_count = 0
            for sub_categ_id in categ.search([('id', 'child_of', categ.ids)]).ids:
                product_count += group_data.get(sub_categ_id, 0)
            categ.product_count = product_count

    def _compute_supplier_count(self):
        read_group_res = self.env['product.supplierinfo'].read_group([('udi_flbm', 'child_of', self.ids)], ['udi_flbm'], ['udi_flbm'])
        group_data = dict((data['udi_flbm'][0], data['udi_flbm_count']) for data in read_group_res)
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

    @api.depends_context('hierarchical_naming')
    def _compute_display_name(self):
        if self.env.context.get('hierarchical_naming', True):
            return super()._compute_display_name()
        for record in self:
            record.display_name = record.name

    @api.ondelete(at_uninstall=False)
    def _unlink_except_default_category(self):
        main_category = self.env.ref('udi_data.medical_device_category_all', raise_if_not_found=False)
        if main_category and main_category in self:
            raise UserError("不能删除此医疗器械分类，它是默认的常规类别。")
