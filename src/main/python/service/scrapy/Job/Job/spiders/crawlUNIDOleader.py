# -*- coding: utf-8 -*-
__author__ = 'chenjialin'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import logging.config
from scrapy.http import Request
from ..allitems.leaderitems import UNIDOLeadersItem
from src.main.python.service.scrapy.Job.Job.utils.strUtil import StrUtil
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil
logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger("ahu")

class UNIDOleader(scrapy.Spider):
    name = "UNIDOleader"
    start_urls = ["http://www.unido.org/who-we-are/structure.html"]

    def __init__(self):
        self.preurl = 'http://www.unido.org'

    def parse(self, response):
        selector = scrapy.Selector(response)
        pdfurl = selector.xpath('//div[@id="main-content"]/div/p/a')
        for pdf in pdfurl:
            item = self._inititem()
            test = pdf.xpath('@href')
            if test:
                test = test.extract()[0]
            else:
                continue

            if test.endswith('.pdf'):
                url = self.preurl + test
                pdf_name = url.split('/')[-1]
                item['pdf_name'] = StrUtil.delWhiteSpace(pdf_name)
                name = pdf.xpath('text()').extract()[0]
                item['name'] = StrUtil.delWhiteSpace(name)
                logger.debug("UNIDO-->leader-->%s" % item['pdf_name'])
                yield Request(url, meta={'item': item}, callback=self.savepdf, dont_filter=True)
                yield item

        url = "http://www.unido.org/fileadmin/user_media_upgrade/Who_we_are/Structure/Director-General/LI_Yong_biography_in_English.pdf"
        item = self._inititem()
        name = 'LI Yong'
        item['name'] = StrUtil.delWhiteSpace(name)
        pdf_name = url.split('/')[-1]
        item['pdf_name'] = StrUtil.delWhiteSpace(pdf_name)
        logger.debug("UNIDO-->leader-->%s" % item['pdf_name'])
        yield Request(url, meta={'item': item}, callback=self.savepdf, dont_filter=True)
        yield item

    def savepdf(self, response):
        item = response.meta['item']
        with open('./UNIDOleaders/' + item['pdf_name'], 'wb') as f:
            f.write(response.body)

    def _inititem(self):
        item = UNIDOLeadersItem()
        item['pdf_name'] = ''
        item['name'] = ''
        return item
