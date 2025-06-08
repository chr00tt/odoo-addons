# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, Command
from odoo.exceptions import RedirectWarning, UserError, ValidationError

class Partner(models.Model):
    _inherit = "res.partner"

    is_manufacturer = fields.Boolean(compute='_compute_is_manufacturer', store=True)

    nhsa_consumables_count = fields.Integer(
        '# 耗材', compute='_compute_nhsa_consumables_count')

    @api.depends('category_id')
    def _compute_is_manufacturer(self):
        manufacturer_category_id = self.env.ref('nhsa_hc.res_partner_category_manufacturer', raise_if_not_found=False)
        if not manufacturer_category_id:
            return
        for record in self:
            category_ids = record.category_id.mapped('id')
            record.is_manufacturer = True if manufacturer_category_id.id in category_ids else False

    @api.model_create_multi
    def create(self, vals_list):
        search_partner_mode = self.env.context.get('res_partner_search_mode')
        if search_partner_mode == 'manufacturer':
            category_id = self.env.ref('nhsa_hc.res_partner_category_manufacturer')
            for vals in vals_list:
                # 设置为机构
                if not vals.get('company_type'):
                    vals['company_type'] = 'company'
                # 添加生产厂家标签
                if not vals.get('category_id'):
                    vals['category_id'] = [Command.link(category_id.id)]
        return super().create(vals_list)

    def _compute_nhsa_consumables_count(self):
        read_group_res = self.env['nhsa.consumables'].read_group([('enterprise', 'in', self.ids)], ['enterprise'], ['enterprise'])
        group_data = dict((data['enterprise'][0], data['enterprise_count']) for data in read_group_res)
        for record in self:
            record.nhsa_consumables_count = group_data.get(record.id, 0)

    @api.model
    def name_create(self, name):
        """ Override of orm's name_create method for partners. The purpose is
            to handle some basic formats to create partners using the
            name_create.
            If only an email address is received and that the regex cannot find
            a name, the name will have the email value.
            If 'force_email' key in context: must find the email address. """
        default_type = self._context.get('default_type')
        if default_type and default_type not in self._fields['type'].get_values(self.env):
            context = dict(self._context)
            context.pop('default_type')
            self = self.with_context(context)
        name, email_normalized = tools.parse_contact_from_email(name)
        if self._context.get('force_email') and not email_normalized:
            raise ValidationError("无法在没有电子邮件地址的情况下创建联系人！")

        create_values = {self._rec_name: name or email_normalized}
        if email_normalized:  # keep default_email in context
            create_values['email'] = email_normalized

        search_partner_mode = self.env.context.get('res_partner_search_mode')
        if search_partner_mode == 'manufacturer':
            # 设置为机构
            if not create_values.get('company_type'):
                create_values['company_type'] = 'company'
            # 添加生产厂家标签
            if not create_values.get('category_id'):
                manufacturer_category = self.env.ref('nhsa_hc.res_partner_category_manufacturer')
                create_values['category_id'] = [(4, manufacturer_category.id)]

        partner = self.create(create_values)
        return partner.id, partner.display_name
