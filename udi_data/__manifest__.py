# -*- coding: utf-8 -*-

{
    'name': '医疗器械唯一标识数据库',
    'author': 'He Jian',
    'website': 'https://github.com/chr00tt/odoo-addons',
    'depends': [
        'product_expiry',
        'stock',

        'product_manufacturer',
        'queue_job',

        'medical_consumables_product',
        'nhsa_hc',
        ],
    'category': 'Inventory/Inventory',
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'data/udi_data_data.xml',
        # 'data/medical.device.category.csv', # 采用异步导入
        'views/ir_cron_views.xml',
        'views/product_views.xml',
        'views/udi_data_views.xml',
        'views/medical_device_category_views.xml',
        'views/stock_menu_views.xml',
        'views/nhsa_consumables_category_views.xml',
        'views/nhsa_consumables_views.xml',
        'views/product_template_views.xml',
    ],
    'post_init_hook': '_udi_data_import_data',
    'license': 'LGPL-3',
}
