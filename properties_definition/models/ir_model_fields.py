# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class IrModelField(models.Model):
    _inherit = 'ir.model.fields'

    definition = fields.Char(
        string='Definition',
        help="The definition record which defined the Properties field definition."
        "For example: team_id.lead_properties_definition")

    def _reflect_field_params(self, field, model_id):
        vals = super(IrModelField, self)._reflect_field_params(field, model_id)
        definition = getattr(field, 'definition', None)
        vals['definition'] = definition
        return vals
    
    def _instanciate_attrs(self, field_data):
        attrs = super(IrModelField, self)._instanciate_attrs(field_data)
        if attrs and field_data.get('definition'):
            attrs['definition'] = field_data['definition']
        return attrs
