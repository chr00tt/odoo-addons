# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class NHSAConsumables(models.Model):
    _inherit = "nhsa.consumables"

    udi_data_count = fields.Integer(
        '# 唯一标识', compute='_compute_udi_data_count')

    def _compute_udi_data_count(self):
        read_group_res = self.env['udi.data'].read_group([('nhsa_consumables_id', 'in', self.ids)], ['nhsa_consumables_id'], ['nhsa_consumables_id'])
        group_data = dict((data['nhsa_consumables_id'][0], data['nhsa_consumables_id_count']) for data in read_group_res)
        for categ in self:
            udi_data_count = 0
            for sub_categ_id in categ.search([('id', 'in', categ.ids)]).ids:
                udi_data_count += group_data.get(sub_categ_id, 0)
            categ.udi_data_count = udi_data_count
