# -*- coding: utf-8 -*-

from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = "account.move"

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
