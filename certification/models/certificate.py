# -*- coding: utf-8 -*-

from odoo import _, fields, models

class Certificate(models.Model):
    _name = 'certificate'
    _description = '资质'
    _inherits = {
        'ir.attachment': 'ir_attachment_id',
    }
    _order = 'name'

    certificate_type_id = fields.Many2one('certificate.type', string='资质类型')
    certificate_number = fields.Char(string='证书编号')
    issue_date = fields.Date(string='发证日期')
    expiry_date = fields.Date(string='到期日期')
    ir_attachment_id = fields.Many2one('ir.attachment', string='资质文件', ondelete='cascade')
    active = fields.Boolean(string='有效', default=True)
