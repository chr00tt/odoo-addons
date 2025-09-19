from odoo import models, fields, api

class MedicalOrder(models.Model):

    _name = 'medical.order'
    _description = '医嘱管理'

    name = fields.Char(string='医嘱名称', required=True)

    patient_id = fields.Many2one('res.partner', string='患者', domain=[('is_patient', '=', True)], required=True)
    doctor_id = fields.Many2one('res.users', string='医生', default=lambda self: self.env.user, required=True)
    date = fields.Datetime(string='开具日期', default=fields.Datetime.now, required=True)
    status = fields.Selection([
        ('draft', '草稿'),
        ('confirmed', '已确认'),
        ('completed', '已完成'),
        ('cancelled', '已取消')
    ], string='状态', default='draft', required=True)
    #diagnosis_id = fields.Many2one('medical.diagnosis', string='诊断')
    # 医嘱内容
    order_lines = fields.One2many('medical.order.line', 'order_id', string='医嘱明细')

    # 说明
    notes = fields.Text(string='备注')

    # 方法
    def action_confirm(self):
        for order in self:
            order.status = 'confirmed'

    def action_complete(self):
        for order in self:
            order.status = 'completed'

    def action_cancel(self):
        for order in self:
            order.status = 'cancelled'
