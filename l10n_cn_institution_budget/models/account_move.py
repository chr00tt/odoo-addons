# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, Command

class AccountMove(models.Model):
    _inherit = "account.move"

    line_ids = fields.One2many(
        'account.move.line',
        'move_id',
        string='财务会计项目',
        copy=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        domain=[('is_budget', '=', False)],
        context={'default_is_budget': False}
    )

    budget_line_ids = fields.One2many(
        'account.move.line',
        'move_id',
        string='预算会计项目',
        copy=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        domain=[('is_budget', '=', True)],
        context={'default_is_budget': True}
    )

    def _get_unbalanced_moves(self, container):
        moves = container['records'].filtered(lambda move: move.line_ids)
        if not moves:
            return

        # /!\ As this method is called in create / write, we can't make the assumption the computed stored fields
        # are already done. Then, this query MUST NOT depend on computed stored fields.
        # It happens as the ORM calls create() with the 'no_recompute' statement.
        self.env['account.move.line'].flush_model(['debit', 'credit', 'balance', 'currency_id', 'move_id'])
        self._cr.execute('''
            SELECT line.move_id,
                   ROUND(SUM(line.debit), currency.decimal_places) debit,
                   ROUND(SUM(line.credit), currency.decimal_places) credit
              FROM account_move_line line
              JOIN account_move move ON move.id = line.move_id
              JOIN res_company company ON company.id = move.company_id
              JOIN res_currency currency ON currency.id = company.currency_id
             WHERE line.move_id IN %s AND line.is_budget = False
          GROUP BY line.move_id, currency.decimal_places
            HAVING ROUND(SUM(line.balance), currency.decimal_places) != 0
        ''', [tuple(moves.ids)])
        result = self._cr.fetchall()
        if result:
            return result

        self.env['account.move.line'].flush_model(['debit', 'credit', 'balance', 'currency_id', 'move_id'])
        self._cr.execute('''
            SELECT line.move_id,
                   ROUND(SUM(line.debit), currency.decimal_places) debit,
                   ROUND(SUM(line.credit), currency.decimal_places) credit
              FROM account_move_line line
              JOIN account_move move ON move.id = line.move_id
              JOIN res_company company ON company.id = move.company_id
              JOIN res_currency currency ON currency.id = company.currency_id
             WHERE line.move_id IN %s AND line.is_budget = True
          GROUP BY line.move_id, currency.decimal_places
            HAVING ROUND(SUM(line.balance), currency.decimal_places) != 0
        ''', [tuple(moves.ids)])
        return self._cr.fetchall()
