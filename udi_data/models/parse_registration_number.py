# -*- coding: utf-8 -*-

import re

from odoo import api, fields, models

class ParseRegistrationNumber(models.AbstractModel):
    _name = 'parse.registration.number'
    _description = '产品注册证号解析'

    def parse_registration_number(self):
        # 注册证编号有可能有多个，提取第1个
        parts = self.registration_number.split(',')
        if parts:
            registration_number = parts[0].strip()
        else:
            registration_number = ''

        res = {}

        pattern = re.compile(r"械注([准进许])")
        match = pattern.search(registration_number)
        if match:
            product_origin_values = {
                '准': 'domestic',
                '进': 'imported',
                '许': 'hongkong_macao_taiwan',
            }
            res['product_origin'] = product_origin_values.get(match.group(1), 'domestic')

        return res
