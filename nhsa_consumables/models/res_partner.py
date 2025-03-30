# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command

class Partner(models.Model):
    _inherit = "res.partner"

    is_manufacturer = fields.Boolean(compute='_compute_is_manufacturer', store=True)

    nhsa_consumables_count = fields.Integer(
        '# 耗材', compute='_compute_nhsa_consumables_count')

    @api.depends('category_id')
    def _compute_is_manufacturer(self):
        manufacturer_category_id = self.env.ref('nhsa_consumables.res_partner_category_manufacturer', raise_if_not_found=False)
        if not manufacturer_category_id:
            return
        for record in self:
            category_ids = record.category_id.mapped('id')
            record.is_manufacturer = True if manufacturer_category_id.id in category_ids else False

    @api.model_create_multi
    def create(self, vals_list):
        search_partner_mode = self.env.context.get('res_partner_search_mode')
        if search_partner_mode == 'manufacturer':
            category_id = self.env.ref('nhsa_consumables.res_partner_category_manufacturer')
            for vals in vals_list:
                vals['category_id'] = [Command.link(category_id.id)]
        return super().create(vals_list)

    def _compute_nhsa_consumables_count(self):
        read_group_res = self.env['nhsa.consumables'].read_group([('enterprise', 'in', self.ids)], ['enterprise'], ['enterprise'])
        group_data = dict((data['enterprise'][0], data['enterprise_count']) for data in read_group_res)
        for record in self:
            record.nhsa_consumables_count = group_data.get(record.id, 0)
