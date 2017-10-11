# -*- coding: utf-8 -*-
__author__ = 'liuyang'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from ..allitems.leaderitems import WIPOLeadersItem
from src.main.python.service.scrapy.Job.Job.utils.strUtil import StrUtil
import logging.config
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil
logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

class WIPOleadersSpider(scrapy.Spider):
    name = "WIPOleaders"

    start_urls = ["http://www.wipo.int/about-wipo/en/management.html"]

    def __init__(self):
        logger.debug("开始爬取WIPO领导人信息")

    def parse(self, response):
        item = self._inititem()
        item["url"] = response.url
        selector = scrapy.Selector(response)

        datas = selector.xpath('//div[@class="content line"]')
        if datas:
            for data in datas[:-1]:

                ns = data.xpath('h2/text()').extract()
                if ns:
                    if '-' in ns[0]:
                        item["name"] = StrUtil.delWhiteSpace(ns[0].split('-')[0])
                        item["section"] = StrUtil.delWhiteSpace(ns[0].split('-')[1])
                    else:
                        item["name"] = StrUtil.delWhiteSpace(ns[0].split('–')[0])
                        item["section"] = StrUtil.delWhiteSpace(ns[0].split('–')[1])

                work = data.xpath('ul[@class="dot__list"]').xpath('string(.)').extract()
                if work:
                    item["work"] = StrUtil.delWhiteSpace(work[0])

                logger.debug('>>>WIPOleader>>>name>>>%s' % item["name"])
                logger.debug('>>>WIPOleader>>>section>>>%s' % item["section"])
                logger.debug('>>>WIPOleader>>>work>>>%s' % item["work"])
                yield item
        else:
            logger.error('爬取WIPO领导人姓名和部门失败')


    def _inititem(self):
        '''
        初始化全部字段
        :return: 初始字段
        '''
        item = WIPOLeadersItem()
        item["work"] = ""
        item["name"] = ""
        item["section"] = ""
        item["englishname"] = "WIPO"
        item["url"] = ""
        logger.info('初始化WIPO领导人item成功')
        return item