# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, _
from odoo.addons.account.models.chart_template import template

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @template('cn_hospital')
    def _get_cn_hospital_template_data(self):
        return {
            'name': '医院',
            'parent': 'cn_institution',
        }
