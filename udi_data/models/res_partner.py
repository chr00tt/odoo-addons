# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, Command
from odoo.exceptions import RedirectWarning, UserError, ValidationError

class Partner(models.Model):
    _inherit = "res.partner"

    udi_data_count = fields.Integer(
        '医疗器械唯一标识数量', compute='_compute_udi_data_count')


    def _compute_udi_data_count(self):
        read_group_res = self.env['udi.data'].read_group([('license_holder', 'in', self.ids)], ['license_holder'],
                                                                 ['license_holder'])
        group_data = dict((data['license_holder'][0], data['license_holder_count']) for data in read_group_res)
        for record in self:
            record.udi_data_count = group_data.get(record.id, 0)

    def action_view_udi_data(self):
        # 可以选择显示通知或保持空操作
        pass