# -*- coding: utf-8 -*-

from odoo import api, fields, models

class FapiaoLine(models.Model):
    _name = "fapiao.line"
    _description = "发票明细"

    fapiao_id = fields.Many2one('fapiao', string='发票', required=True, ondelete='cascade')

    name = fields.Char(string='名称')

    move_line_id = fields.Many2one('account.move.line', string='账单明细', required=True, ondelete='cascade')
    amount = fields.Monetary(string='Amount', required=True, currency_field='currency_id')
    currency_id = fields.Many2one(related='fapiao_id.currency_id', store=True, readonly=True)
    description = fields.Char(string='Description')

    @api.model_create_multi
    def create(self, vals_list):
        return super(FapiaoLine, self).create(vals_list)
