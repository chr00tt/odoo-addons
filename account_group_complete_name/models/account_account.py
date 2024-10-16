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
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name
