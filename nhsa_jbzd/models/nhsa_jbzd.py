# -*- coding: utf-8 -*-

from odoo import api, models, fields, _, SUPERUSER_ID

class NhsaJbzd(models.Model):
    _name = 'nhsa.jbzd'
    _description = '手术操作代码'

    code = fields.Char('编码', True, required=True)
    master_code = fields.Boolean('主要编码', default=False)
    name = fields.Char('名称', index='trigram', required=True)
    category = fields.Selection([
        ('1', '治疗性操作'),
        ('2', '操作'),
        ('3', '检查'),
        ('4', '治疗'),
        ('5', '其他'),
    ], string='类别', required=True, default='1')
