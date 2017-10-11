# -*- coding: utf-8 -*-
__author__ = 'Robin'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy

try:
    from pydispatch import dispatcher
except:
    from scrapy.xlib.pydispatch import dispatcher
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil
import logging.config
from scrapy.http import Request

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')
path = u"WMO.csv"

class WMOjobsSpider(scrapy.Spider):

    name = 'WMOjobs'
    start_urls = ['https://erecruit.wmo.int/public/']

    def __init__(self):
        logger.debug('开始爬取WMO岗位信息')
        self.items = []
        self.url = 'https://erecruit.wmo.int/public/'
        # dispatcher.connect(self.spider_closed,signels.spider_closed)

    def parse(self, response):
        selector = scrapy.Selector(response)
        frlinks = selector.xpath("//div[@id='login']/table/tr/td[2]/table[last()]//tr/td[last()]/a/@href").extract()
        print frlinks
        enlinks = [link[:-2]+'en' for link in frlinks]
        for link in enlinks:
            nexturl = self.url + link
            print 'next url is ', nexturl
            yield Request(url=nexturl, callback=self.parseDetail)
    
    def parseDetail(self, response):
        selector = scrapy.Selector(response)
        trs = selector.xpath("//table[@valign='top']")
        # print trs.extract()

    def _initItem(self):
        pass

    def spider_closed(self):
        pass
    