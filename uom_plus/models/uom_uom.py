# -*- coding: utf-8 -*-

from odoo import api, fields, tools, models, _

class UoM(models.Model):
    _inherit = 'uom.uom'

    @api.model
    def name_create(self, name):
        """ The UoM category and factor are required, so we'll have to add temporary values
        for imported UoMs """
        values = {
            self._rec_name: name,
            'factor': 1,
            # Fix ValidationError: UoM category %s should only have one reference unit of measure.
            'uom_type': 'bigger',
        }
        # look for the category based on the english name, i.e. no context on purpose!
        # TODO: should find a way to have it translated but not created until actually used
        if not self._context.get('default_category_id'):
            EnglishUoMCateg = self.env['uom.category'].with_context({})
            misc_category = EnglishUoMCateg.search([('name', '=', '未分类/导入的单位')])
            if misc_category:
                values['category_id'] = misc_category.id
            else:
                values['category_id'] = EnglishUoMCateg.name_create('未分类/导入的单位')[0]
                # Fix ValidationError: UoM category %s should have a reference unit of measure.
                values['uom_type'] = 'reference'
        new_uom = self.create(values)
        return new_uom.id, new_uom.display_name
