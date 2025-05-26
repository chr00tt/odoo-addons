# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command

class ResPartner(models.Model):
    _inherit = 'res.partner'

    certificate_ids = fields.One2many('partner.certificate', 'partner_id', '资质')
