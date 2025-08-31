# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    registration_number = fields.Char('注册证编号或者备案凭证编号', tracking=True)
    registration_start_date = fields.Date('注册证开始日期', tracking=True)
    registration_validity_period = fields.Date('注册证有效期', tracking=True)

    def check_registration_validity(self):
        today = fields.Date.today()
        expired_products = self.search([
            ('registration_validity_period', '<', today),
            ('registration_validity_period', '!=', False)
        ])
        for record in expired_products:
            error_msg = f"产品 {record.name} 的注册证已于 {record.registration_validity_period} 过期，请及时处理。"
            existing_activity = self.env['mail.activity'].search([
                ('res_id', '=', record.id),
                ('res_model_id', '=', self.env.ref('product.model_product_template').id),
                ('note', '=', error_msg),
            ])
            if not existing_activity:
                self.env['mail.activity'].create({
                    'res_id': record.id,
                    'res_model_id': self.env.ref('product.model_product_template').id,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_warning').id,
                    'summary': '注册证过期提醒',
                    'note': error_msg,
                    'date_deadline': today,
                    'user_id': self.env.user.id,
                })
        return True
