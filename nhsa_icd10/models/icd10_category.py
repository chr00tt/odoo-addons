# -*- coding: utf-8 -*-

from odoo import models, api, fields

class Icd10Category(models.Model):
    _name = 'icd10.category'
    _description = 'ICD-10 分类'
    _rec_name = 'complete_name'

    name = fields.Char(string='名称', required=True)
    code = fields.Char(string='分类代码', required=True, index=True)
    parent_id = fields.Many2one('icd10.category', '上级分类', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True, unaccent=False)
    child_id = fields.One2many('icd10.category', 'parent_id', '下级分类')
    code_count = fields.Integer(
        '# 代码', compute='_compute_code_count',
        help="该分类下的ICD-10代码数量（不包括子分类）")
    complete_name = fields.Char(
        '完整名称', compute='_compute_complete_name', recursive=True,
        store=True)

    def _compute_code_count(self):
        read_group_res = self.env['icd10.code']._read_group([('category_id', 'child_of', self.ids)], ['category_id'], ['__count'])
        group_data = {categ.id: count for categ, count in read_group_res}
        for categ in self:
            code_count = 0
            for sub_categ_id in categ.search([('id', 'child_of', categ.ids)]).ids:
                code_count += group_data.get(sub_categ_id, 0)
            categ.code_count = code_count

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    @api.depends_context('hierarchical_naming')
    def _compute_display_name(self):
        if self.env.context.get('hierarchical_naming', True):
            return super()._compute_display_name()
        for record in self:
            record.display_name = record.name