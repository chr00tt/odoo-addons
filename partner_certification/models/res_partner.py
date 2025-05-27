# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command

class ResPartner(models.Model):
    _inherit = 'res.partner'

    certificate_ids = fields.One2many('certificate', 'res_id', '资质')
    certificate_count = fields.Integer(compute='_compute_certificate_count', string='资质数量')

    def _compute_certificate_count(self):
        for record in self:
            record.certificate_count = record.env['certificate'].search_count([
                ('res_model', '=', 'res.partner'),
                ('res_id', '=', record.id),
            ])

    def action_open_certificates(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': '资质',
            'res_model': 'certificate',
            'view_mode': 'kanban,tree,form',
            'context': {
                'default_res_model': self._name,
                'default_res_id': self.id,
                'default_company_id': self.company_id.id,
            },
            'domain': [('res_model', '=', 'res.partner'), ('res_id', '=', self.id)],
        }
