# -*- coding: utf-8 -*-

from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = "account.move"

    fapiao_count = fields.Integer(compute="_compute_fapiao", string='发票数量', copy=False, default=0, store=True)
    fapiao_ids = fields.Many2many('fapiao', compute="_compute_fapiao", string='发票', copy=False, store=True)

    @api.depends('line_ids.fapiao_lines.fapiao_id')
    def _compute_fapiao(self):
        for record in self:
            fapiaos = record.mapped('line_ids.fapiao_lines.fapiao_id')
            record.fapiao_ids = fapiaos
            record.fapiao_count = len(fapiaos)

    def action_create_fapiao(self):
        for move in self:
            if move.move_type != 'in_invoice':
                continue

            move = move.with_company(move.company_id)

            # TODO


        fapiao = self.env['fapiao.fapiao'].create({
            'move_id': self.id,
            'partner_id': self.partner_id.id,
            'amount': self.amount_total,
            'date': fields.Date.today(),
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'fapiao.fapiao',
            'res_id': fapiao.id,
            'view_mode': 'form',
            'target': 'current',
        }
