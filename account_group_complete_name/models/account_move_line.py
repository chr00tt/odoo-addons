from odoo import api, fields, models, Command, _

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    account_group_complete_name = fields.Char("科目组", related="account_id.group_id.complete_name")
