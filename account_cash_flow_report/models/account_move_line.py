# -*- coding: utf-8 -*-
from odoo import api, fields, models, Command, _

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    tag_ids = fields.Many2many('account.account.tag', 'move_account_account_tag', string='标签', compute='_compute_tag_ids', store=True, readonly=False, precompute=True, ondelete='restrict')

    @api.depends('account_id')
    def _compute_tag_ids(self):
        for record in self:
            if record.account_id:
                record.tag_ids = record.account_id.tag_ids

