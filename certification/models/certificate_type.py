# -*- coding: utf-8 -*-

from odoo import _, api, exceptions, fields, models, tools, registry, SUPERUSER_ID, Command

class CerticateType(models.Model):
    _name = 'certificate.type'
    _description = '资质类型'
    _order = 'sequence, name'

    name = fields.Char(string='名称', required=True)
    code = fields.Char(string='编号', required=True, help='Unique code for the certificate type')
    sequence = fields.Integer(string='序号', default=10, help='Sequence for ordering certificate types')
    description = fields.Text(string='描述', help='Description of the certificate type')
    active = fields.Boolean(string='启用', default=True, help='Indicates if the certificate type is active')
    
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The code must be unique for each certificate type.'),
    ]
