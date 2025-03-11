# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

import feedparser
import logging
import requests
import tempfile
import os
import zipfile
from lxml import etree

UDID_DAILY_RSS_URL = "https://udi.nmpa.gov.cn//rss/download.html?files=daily"
UDID_WEEKLY_RSS_URL = "https://udi.nmpa.gov.cn/rss/download.html?files=weekly"
UDID_MONTHLY_RSS_URL = "https://udi.nmpa.gov.cn/rss/download.html?files=monthly"

class RssMixin(models.AbstractModel):
    _name = 'rss.mixin'
    _description = 'RSS Mixin'

    def do_daily_update(self):
        self._do_update(UDID_DAILY_RSS_URL)

    def do_weekly_update(self):
        self._do_update(UDID_WEEKLY_RSS_URL)

    def do_monthly_update(self):
        self._do_update(UDID_MONTHLY_RSS_URL)

    def _do_update(self, rss_url):
        try:
            rss = feedparser.parse(rss_url)
            entry = rss.entries[0]
            link = entry.link

            zip_path = self._download_zip(link)

            extract_dir = tempfile.mkdtemp()
            with zipfile.ZipFile(zip_path) as zip_ref:
                zip_ref.extractall(extract_dir)

            self._import_data_files(extract_dir)
            os.unlink(zip_path)
        except Exception as e:
            logging.error("医疗器械唯一标识数据更新错误: %s" % str(e))

    def _download_zip(self, link):
        response = requests.get(link)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(response.content)
            tmp_file.close()
            return tmp_file.name

    def _import_data_files(self, directory):
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.xml'):
                    self._import_xml(os.path.join(root, file))
                    break

    def _import_xml(self, file_path):
        udi_data_sudo = self.env['udi.data'].sudo()
        udi_data_list = []

        content = etree.iterparse(file_path, events=('end',), tag='device')
        for _, elem in content:
            key = elem.findtext('zxxsdycpbs')
            record = udi_data_sudo.search([('zxxsdycpbs', '=', key)])
            if record:
                record.write(self._create_record(elem))
            else:
                udi_data_list.append(self._create_record(elem))
            elem.clear()

        if udi_data_list:
            udi_data_sudo.create(udi_data_list)
            
    def _create_record(self, elem):
        return {
            'zxxsdycpbs': elem.findtext('zxxsdycpbs'),
            'cpbsbmtxmc': elem.findtext('cpbsbmtxmc'),
            'cpbsfbrq': elem.findtext('cpbsfbrq'),
            'zxxsdyzsydydsl': elem.findtext('zxxsdyzsydydsl'),
            'sydycpbs': True if elem.findtext('sydycpbs') == '是' else False,
            'cpmctymc': elem.findtext('cpmctymc'),
            'spmc': elem.findtext('spmc'),
            'ggxh': elem.findtext('ggxh'),
            'sfwblztlcp': True if elem.findtext('sfwblztlcp') == '是' else False,
            'cpms': elem.findtext('cpms'),
            'cphhhbh': elem.findtext('cphhhbh'),
            'yflbm': elem.findtext('yflbm'),
            'flbm': elem.findtext('flbm'),
            'ylqxzcrbarmc': elem.findtext('ylqxzcrbarmc'),
            'ylqxzcrbarywmc': elem.findtext('ylqxzcrbarywmc'),
            'tyshxydm': elem.findtext('tyshxydm'),
            'zczbhhzbapzbh': elem.findtext('zczbhhzbapzbh'),
            'ybbm': elem.findtext('ybbm'),
            'cplb': elem.findtext('cplb'),
            'cgzmraqxgxx': elem.findtext('cgzmraqxgxx'),
            'sfbjwycxsy': True if elem.findtext('sfbjwycxsy') == '是' else False,
            'zdcfsycs': elem.findtext('zdcfsycs'),
            'sfwwjbz': True if elem.findtext('sfwwjbz') == '是' else False,
            'syqsfxyjxmj': True if elem.findtext('syqsfxyjxmj') == '是' else False,
            'mjfs': elem.findtext('mjfs'),
            'deviceRecordKey': elem.findtext('deviceRecordKey'),
            'versionNumber': elem.findtext('versionNumber'),
            'tsrq': elem.findtext('tsrq'),
            'versionTime': elem.findtext('versionTime'),
        }