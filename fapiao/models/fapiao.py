# -*- coding: utf-8 -*-

from odoo import api, fields, models

class Fapiao(models.Model):
    _name = 'fapiao'
    _description = '发票'
    _order = 'date desc'

    type = fields.Selection([
        ('01', '增值税专用发票'),
        ('04', '增值税普通发票'),
    ], string='类型', default='01')
    code = fields.Char('代码', help='税务部门给予发票的编码，用于发票的管理和核查。')
    name = fields.Char('号码', required=True, copy=False, index=True, help='发票的唯一编号。')
    date = fields.Date('开票日期')
    amount = fields.Monetary(string='金额', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='币种', required=True, default=lambda self: self.env.company.currency_id)
