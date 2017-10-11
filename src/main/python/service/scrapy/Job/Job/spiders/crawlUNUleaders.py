# -*- coding: utf-8 -*-
__author__ = 'chenjialin'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from ..allitems.leaderitems import UNULeadersItem
from src.main.python.service.scrapy.Job.Job.utils.strUtil import StrUtil
import logging.config
from scrapy.http import Request
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

class UNUleaderSpider(scrapy.Spider):
    name = "UNUleaders"

    start_urls = ["https://unu.edu/about/unu/office-of-the-rector",   #校长办公室
                 "https://unu.edu/about/unu/management-group",    #管理组
                 "https://unu.edu/about/unu-council"]           #理事会

    def __init__(self):
        logger.debug("开始爬取UNU领导人信息")
        self.url = "https://www.unu.edu/"

    def parse(self, response):
        selector = scrapy.Selector(response)

        if response.url.endswith('office-of-the-rector'):
            logger.info("打开校长办公室页面成功，开始爬取校长办公室成员")
            pes = selector.xpath('//ul[@class="persons"]/li/a')
            i = 0
            for pe in pes:
                i += 1
                try:
                    url = pe.xpath('@href').extract()[0]
                    logger.debug("开始爬取第%d位校长办公室成员"%i)
                    yield Request(url=url,callback=self._parseRectorOffice)
                except:
                    pass
            logger.info("共爬取%d位校长办公室成员信息"%i)


        elif response.url.endswith('management-group'):
            logger.info("打开管理组页面成功，开始爬取管理组成员")
            pes = selector.xpath('//ul[@class="persons"]/li/a')
            i = 0
            for pe in pes:
                i += 1
                try:
                    url = pe.xpath('@href').extract()[0]
                    logger.debug("开始爬取第%d位管理组成员" % i)
                    yield Request(url=url, callback=self._parseManagement)
                except:
                    pass
            logger.info("共爬取%d位管理组成员信息" % i)

        elif response.url.endswith('unu-council'):
            logger.info("打开理事会页面成功，开始爬取理事会成员")
            pes = selector.xpath('//ul[@class="persons"]/li/a')
            i = 0
            for pe in pes:
                i += 1
                try:
                    url = pe.xpath('@href').extract()[0]
                    logger.debug("开始爬取第%d位理事会成员" % i)
                    yield Request(url=url, callback=self._parseCouncil)
                except:
                    pass
            logger.info("共爬取%d位理事会成员信息" % i)

    def _parseRectorOffice(self,response):
        '''
        校长办公室
        :return:
        '''
        selector = scrapy.Selector(response)
        item = self._inititem()
        item["url"] = response.url

        name = selector.xpath('//section[@class="eight phone-four columns "]/h1/text()').extract()
        if name:
            item["name"] = StrUtil.delWhiteSpace(name[0])
            logger.debug('>>UNU>>leader>>name>>%s'%item["name"])
        else:
            logger.error('爬取UNU领导人姓名失败，网页结构可能改变，建议检查')

        work = selector.xpath('//section[@class="eight phone-four columns "]/h4/text()').extract()
        if work:
            item["work"] = StrUtil.delWhiteSpace(work[0])
        else:
            logger.error('爬取校长办公室成员职位出错')

        resume = selector.xpath('//section[@class="eight phone-four columns "]/div/ul/li/div').xpath('string(.)').extract()
        if resume:
            item["resume"] = StrUtil.delWhiteSpace(resume[0])
        else:
            logger.error('爬取校长办公室成员简历出错')

        logger.debug('>>>OECDleader>>>校长办公室成员work>>>%s' % item["work"])
        logger.debug('>>>OECDleader>>>校长办公室成员name>>>%s' % item["name"])
        logger.debug('>>>OECDleader>>>校长办公室成员resume>>>%s' % item["resume"])
        yield item

    def _parseManagement(self,response):
        '''
        管理组
        :return:
        '''
        selector = scrapy.Selector(response)
        item = self._inititem()
        item["url"] = response.url

        name = selector.xpath('//section[@class="eight phone-four columns "]/h1/text()').extract()
        if name:
            item["name"] = StrUtil.delWhiteSpace(name[0])
            logger.debug('>>UNU>>leader>>name>>%s'%item["name"])
        else:
            logger.error('爬取UNU领导人姓名失败，网页结构可能改变，建议检查')

        work = selector.xpath('//section[@class="eight phone-four columns "]/h4/text()').extract()
        if work:
            item["work"] = StrUtil.delWhiteSpace(work[0])
        else:
            logger.error('爬取管理组成员职位出错')

        resume = selector.xpath('//section[@class="eight phone-four columns "]/div/ul/li/div').xpath('string(.)').extract()
        if resume:
            item["resume"] = StrUtil.delWhiteSpace(resume[0])
        else:
            logger.error('爬取管理组成员简历出错')

        logger.debug('>>>OECDleader>>>管理组成员work>>>%s' % item["work"])
        logger.debug('>>>OECDleader>>>管理组成员name>>>%s' % item["name"])
        logger.debug('>>>OECDleader>>>管理组成员resume>>>%s' % item["resume"])
        yield item

    def _parseCouncil(self,response):
        '''
        理事会
        :return:
        '''
        selector = scrapy.Selector(response)
        item = self._inititem()
        item["url"] = response.url

        name = selector.xpath('//section[@class="eight phone-four columns "]/h1/text()').extract()
        if name:
            item["name"] = StrUtil.delWhiteSpace(name[0])
            logger.debug('>>UNU>>leader>>name>>%s'%item["name"])
        else:
            logger.error('爬取UNU领导人姓名失败，网页结构可能改变，建议检查')

        work = selector.xpath('//section[@class="eight phone-four columns "]/h4/text()').extract()
        if work:
            item["work"] = StrUtil.delWhiteSpace(work[0])
        else:
            logger.error('爬取理事会成员职位出错')

        resume = selector.xpath('//section[@class="eight phone-four columns "]/div/ul/li/div').xpath('string(.)').extract()
        if resume:
            item["resume"] = StrUtil.delWhiteSpace(resume[0])
        else:
            logger.error('爬取理事会成员简历出错')

        logger.debug('>>>OECDleader>>>理事会成员work>>>%s' % item["work"])
        logger.debug('>>>OECDleader>>>理事会成员name>>>%s' % item["name"])
        logger.debug('>>>OECDleader>>>理事会成员resume>>>%s' % item["resume"])
        yield item

    def _inititem(self):
        '''
        初始化全部字段
        :return: 初始字段
        '''
        item = UNULeadersItem()
        item["work"] = ""
        item["name"] = ""
        item["resume"] = ""
        item["englishname"] = "UNU"
        item["url"] = ""
        logger.info('初始化UNU领导人item成功')
        return item