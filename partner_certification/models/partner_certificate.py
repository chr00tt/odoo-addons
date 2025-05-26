# -*- coding: utf-8 -*-

from odoo import _, fields, models

class PartnerCertificate(models.Model):
    _name = 'partner.certificate'
    _description = '资质'
    _inherit = 'certificate'

    partner_id = fields.Many2one('res.partner', '联系人',
                                  index=True, ondelete='cascade')
