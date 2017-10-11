# -*- coding: utf-8 -*-
__author__ = 'liuyang'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import re
from scrapy.http import Request
from ..allitems.leaderitems import OECDLeadersItem
from src.main.python.service.scrapy.Job.Job.utils.strUtil import StrUtil
import logging.config
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

class OECDleadersSpider(scrapy.Spider):
    name = "OECDleaders"

    allowed_domains = ["www.oecd.org"]

    start_urls = ["http://www.oecd.org/about/secretary-general/",
                  "http://www.oecd.org/about/whodoeswhat/photos-cvs-deputy-secretary-generals.htm",
                  "http://www.oecd.org/about/whodoeswhat/gabriela-ramos.htm",
                  "http://www.oecd.org/about/whodoeswhat/omar-baig.htm",
                  "http://www.oecd.org/about/whodoeswhat/photos-cv-directors.htm"]

    def __init__(self):
        logger.debug("开始爬取OECD领导人信息")
        self.url = "http://www.oecd.org"

    def parse(self, response):
        selector = scrapy.Selector(response)
        if response.url.endswith('secretary-general/'):   # todo 秘书长
            logger.info("打开秘书长页面成功，开始爬取秘书长信息")
            cv = selector.xpath('//div[@id="webEditContent"]/table[1]/tbody/tr/td[2]/ul[1]/li[1]/a[1]/@href').extract()
            if cv:
                url = self.url + cv[0]
                logger.debug("开始爬取秘书长简历")
                yield Request(url=url,callback=self._parseSecretaryGeneral)

        elif response.url.endswith('photos-cvs-deputy-secretary-generals.htm'):   # todo 副秘书长
            logger.info("打开副秘书长页面成功，开始爬取副秘书长信息")
            cvs = selector.xpath('//div[@id="webEditContent"]/p/a')
            i = 0
            for cv in cvs:
                try:
                    if cv.xpath('text()').extract()[0] == 'CV':
                        i += 1
                        url = self.url + cv.xpath('@href').extract()[0]
                        logger.debug("开始爬取第%d位副秘书长"%i)
                        yield Request(url=url,callback=self._parseDeputySecretariesGeneral)
                except:
                    pass
            logger.info("共爬取%d位副秘书长简历"%i)

        elif response.url.endswith('gabriela-ramos.htm'):           # todo 总参谋长
            logger.info("打开总参谋长页面成功，开始爬取总参谋长信息")
            item = self._inititem()
            item["work"] = "ChiefofStaff"
            item["url"] = response.url

            name = selector.xpath('//div[@class="col-sm-9 leftnav-content-wrapper"]/h1/text()').extract()
            if name:
                try:
                    item["name"] = StrUtil.delWhiteSpace(name[0].split(',')[0])
                except:
                    logger.warning('总参谋长页面可能变化，建议检查')
                    item["name"] = StrUtil.delWhiteSpace(name[0])
            else:
                logger.error('爬取总参谋长姓名出错')

            resume = selector.xpath('//div[@id="webEditContent"]/table[1]').xpath('string(.)').extract()
            if resume:
                item["resume"] = StrUtil.delWhiteSpace(resume[0]).strip('Click here for high-resolution photo')
            else:
                logger.error('爬取总参谋长简历出错')

            logger.debug('>>>OECDleader>>>总参谋长work>>>%s'%item["work"])
            logger.debug('>>>OECDleader>>>总参谋长name>>>%s'%item["name"])
            logger.debug('>>>OECDleader>>>总参谋长resume>>>%s'%item["resume"])
            yield item

        elif response.url.endswith('omar-baig.htm'):  # todo 执行董事
            logger.info("打开执行董事页面成功，开始爬取执行董事信息")
            item = self._inititem()
            item["work"] = "ExecutiveDirector"
            item["url"] = response.url

            name = selector.xpath('//div[@class="col-sm-9 leftnav-content-wrapper"]/h1/text()').extract()
            if name:
                try:
                    item["name"] = StrUtil.delWhiteSpace(name[0].split(',')[0])
                except:
                    logger.warning('执行董事页面可能变化，建议检查')
                    item["name"] = StrUtil.delWhiteSpace(name[0])
            else:
                logger.error('爬取执行董事姓名出错')

            resume = selector.xpath('//div[@id="webEditContent"]').xpath('string(.)').extract()
            if resume:
                item["resume"] = StrUtil.delWhiteSpace(resume[0])
            else:
                logger.error('爬取执行董事简历出错')

            logger.debug('>>>OECDleader>>>执行董事work>>>%s' % item["work"])
            logger.debug('>>>OECDleader>>>执行董事name>>>%s' % item["name"])
            logger.debug('>>>OECDleader>>>执行董事resume>>>%s' % item["resume"])
            yield item

        elif response.url.endswith('photos-cv-directors.htm'):  # todo 董事
            cvs = selector.xpath('//div[@id="webEditContent"]//a')
            i = 0
            for cv in cvs:
                try:
                    if cv.xpath('text()').extract()[0] == 'CV':
                        i += 1
                        ur = cv.xpath('@href').extract()[0]
                        if ur.startswith('/'):
                            url = self.url + ur
                        else:
                            url = ur
                        logger.debug("开始爬取第%d位董事" % i)
                        yield Request(url=url, callback=self._parseDirectors)
                except:
                    pass
            logger.info("共爬取%d位董事" % i)

    def _parseDirectors(self,response):
        '''
        董事
        :return: 
        '''
        selector = scrapy.Selector(response)
        item = self._inititem()
        item["work"] = "Directors"
        item["url"] = response.url

        name = selector.xpath('//div[@class="col-sm-9 leftnav-content-wrapper"]/h1/text()').extract()
        if name:
            name[0] = re.sub('-',',',name[0])
            try:
                item["name"] = StrUtil.delWhiteSpace(name[0].split(',')[0])
            except:
                logger.warning('董事页面可能变化，建议检查')
                item["name"] = StrUtil.delWhiteSpace(name[0])
        elif response.url == "http://www.oecd.org/legal/nicola-bonucci-cv.htm":
            name = selector.xpath('//div[@class="span-19 last"]/h1/text()').extract()[0]
            item["name"] = StrUtil.delWhiteSpace(name.split(',')[0])
        else:
            logger.error('爬取董事姓名出错')

        resume = selector.xpath('//div[@id="webEditContent"]').xpath('string(.)').extract()
        if resume:
            item["resume"] = StrUtil.delWhiteSpace(resume[0])
        else:
            logger.error('爬取董事简历出错')

        logger.debug('>>>OECDleader>>>董事work>>>%s' % item["work"])
        logger.debug('>>>OECDleader>>>董事name>>>%s' % item["name"])
        logger.debug('>>>OECDleader>>>董事resume>>>%s' % item["resume"])
        yield item


    def _parseDeputySecretariesGeneral(self,response):
        '''
        副秘书长
        '''
        selector = scrapy.Selector(response)
        item = self._inititem()
        item["work"] = "DeputySecretariesGeneral"
        item["url"] = response.url

        name = selector.xpath('//div[@class="col-sm-9 leftnav-content-wrapper"]/h1/text()').extract()
        if name:
            try:
                item["name"] = StrUtil.delWhiteSpace(name[0].split(',')[0])
            except:
                logger.warning('副秘书长页面可能变化，建议检查')
                item["name"] = StrUtil.delWhiteSpace(name[0])
        else:
            logger.error('爬取副秘书长姓名出错')

        resume = selector.xpath('//div[@id="webEditContent"]').xpath('string(.)').extract()
        if resume:
            item["resume"] = StrUtil.delWhiteSpace(resume[0]).strip('Click here for high-resolution')
        else:
            logger.error('爬取副秘书长简历出错')

        logger.debug('>>>OECDleader>>>副秘书长work>>>%s' % item["work"])
        logger.debug('>>>OECDleader>>>副秘书长name>>>%s' % item["name"])
        logger.debug('>>>OECDleader>>>副秘书长resume>>>%s' % item["resume"])
        yield item

    def _parseSecretaryGeneral(self,response):
        '''
        秘书长
        '''
        selector = scrapy.Selector(response)
        item = self._inititem()
        item["work"] = "SecretaryGeneral"
        item["url"] = response.url

        name = selector.xpath('//div[@class="col-sm-9 leftnav-content-wrapper"]/h1[@class="ip-title"]/text()').extract()
        if name:
            try:
                item["name"] = StrUtil.delWhiteSpace(name[0].split(',')[0])
            except:
                logger.warning('秘书长页面可能发生变化，建议检查')
                item["name"] = StrUtil.delWhiteSpace(name[0])
        else:
            logger.error('爬取秘书长姓名出错')

        resume = selector.xpath('//div[@id="webEditContent"]/table[1]').xpath('string(.)').extract()
        if resume:
            item["resume"] = StrUtil.delWhiteSpace(resume[0]).strip('More photos of Mr. Gurría   ')
        else:
            logger.error('爬取秘书长简历出错')

        logger.debug('>>>OECDleader>>>秘书长work>>>%s' % item["work"])
        logger.debug('>>>OECDleader>>>秘书长name>>>%s' % item["name"])
        logger.debug('>>>OECDleader>>>秘书长resume>>>%s' % item["resume"])
        yield item

    def _inititem(self):
        '''
        初始化全部字段
        :return: 初始化字段
        '''
        item = OECDLeadersItem()
        item["work"] = ""
        item["name"] = ""
        item["resume"] = ""
        item["englishname"] = "OECD"
        item["url"] = ""
        logger.info('初始化OECD领导人item成功')
        return item