from odoo import models, fields, api

class MedicalOrderLine(models.Model):
    _name = 'medical.order.line'
    _description = '医嘱明细'

    order_id = fields.Many2one('medical.order', string='医嘱', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='耗材')
    quantity = fields.Float(string='数量', default=1)
    usage = fields.Text(string='使用说明')
    frequency = fields.Selection([
        ('once', '一次'),
        ('twice', '两次'),
        ('thrice', '三次'),
        ('other', '其他')
    ], string='频率')
    duration = fields.Integer(string='持续时间（天）')