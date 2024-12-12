# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    geoloc_provider_amap_key = fields.Char(
        string='高德 API Key',
        config_parameter='amap_geolocalize.amap_api_key',
        help="Visit https://lbs.amap.com/api/webservice/create-project-and-key for more information."
    )
