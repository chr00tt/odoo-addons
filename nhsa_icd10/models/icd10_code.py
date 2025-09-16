# -*- coding: utf-8 -*-

from odoo import models, api, fields

class Icd10Code(models.Model):
    _name = 'icd10.code'
    _description = 'ICD-10 Code'
    _rec_name = 'code'

    code = fields.Char(string='编号', required=True, index=True)
    name = fields.Char(string='名称', required=True)
    category_id = fields.Many2one('icd10.category', string='分类', index=True)
