# -*- coding: utf-8 -*-
__author__ = 'liuyang'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from ..allitems.leaderitems import UNDPLeadersItem
from src.main.python.service.scrapy.Job.Job.utils.strUtil import StrUtil
import logging.config
from scrapy.http import Request
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

class UNDPleadersSpider(scrapy.Spider):
    name = "UNDPleaders"

    start_urls = ["http://www.undp.org/content/undp/en/home/operations/leadership/RBAS.html"]

    def __init__(self):
        logger.debug("开始爬取UNDP领导人信息")
        self.preurl = 'http://www.undp.org'

    def parse(self, response):
        selector = scrapy.Selector(response)
        links = selector.xpath('//div[@class="presscenterLeftNav"]/ul/li')
        i = 0
        for link in links:
            leader = link.xpath('a/@href').extract()
            print leader
            if leader:
                url = self.preurl + leader[0]
                yield Request(url=url,callback=self.leaderParse)
                i += 1
                logger.debug('已爬取第%d位领导人'%i)
        logger.debug('爬取UNDP领导人结束，共爬取%d位领导人'%i)

    def leaderParse(self, response):
        item = self._inititem()
        item["url"] = response.url
        selector = scrapy.Selector(response)

        name = selector.xpath('//div[@class="section titleStory"]').xpath('string(.)').extract()
        if name:
            item["name"] = StrUtil.delWhiteSpace(name[0])
            logger.debug('>>UNDP>>leader>>name>>%s'%item["name"])
        else:
            logger.error('爬取UNDP领导人姓名失败，网页结构可能改变，建议检查')

        work = selector.xpath('//div[@class="section h3Story"]').xpath('string(.)').extract()
        if work:
            item["work"] = StrUtil.delWhiteSpace(work[0])
            logger.debug('>>UNDP>>leader>>work>>%s'%item["work"])
        else:
            logger.error('爬取UNDP领导人职位失败，网页结构可能改变，建议检查')

        resume = selector.xpath('//div[@class="parbase section textimage"]').xpath('string(.)').extract()
        if resume:
            item["resume"] = ' '.join(StrUtil.delWhiteSpace(resume[0]).split())
            logger.debug('>>UNDP>>leader>>resume>>%s'%item["resume"])
        else:
            logger.error('爬取UNDP领导人简历失败，网页结构可能改变，建议检查')
        yield item

    def _inititem(self):
        '''
        初始化全部字段
        :return: 初始字段
        '''
        item = UNDPLeadersItem()
        item["work"] = ""
        item["name"] = ""
        item["resume"] = ""
        item["englishname"] = "WIPO"
        item["url"] = ""
        logger.info('初始化UNDP领导人item成功')
        return item