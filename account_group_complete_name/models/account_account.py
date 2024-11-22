from odoo import api, fields, models, _, tools

class AccountGroup(models.Model):
    _inherit = "account.group"

    complete_name = fields.Char(
        '全名', compute='_compute_complete_name', recursive=True,
        store=True)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = "%(parent)s / %(own)s" % {
                    "parent": category.parent_id.complete_name,
                    "own": category.name,
                }
            else:
                category.complete_name = category.name

    def _adapt_parent_account_group(self):
        super(AccountGroup, self)._adapt_parent_account_group()

        if self:
            self.env.add_to_compute(self._fields['complete_name'], self.search([]))
