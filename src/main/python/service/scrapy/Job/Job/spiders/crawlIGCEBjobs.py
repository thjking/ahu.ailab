# -*- coding: utf-8 -*-
#writen by Jing
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from ..allitems.jobitems import ICGEBjobDataItem
from src.main.python.service.scrapy.Job.Job.utils.strUtil import StrUtil
import logging.config
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

class IGCEBjobSpider(scrapy.Spider):
    name = "IGCEBjobs"

    allowed_domins = ["http://www.icgeb.org/home-nd.html"]

    start_urls = ["http://www.icgeb.org/vacancies.html"]

    def __init__(self):
        logger.debug("开始爬取IGCEB工作信息")
        self.url = "http://www.icgeb.org/vacancies.html"

    def parse(self, response):
        item = self._inititem()
        item["joburl"] = response.url
        selector = scrapy.Selector(response)
        links = selector.xpath('//div[@class="ce_text block"]')
        print links.__len__()

        locationTemp = ""
        requireTemp = ""
        workTemp = ""
        deadlineTemp = ""
        applymethodTemp = ""

        if links:
            for i in range(1,len(links)):   #从第二个开始
                print i
    #            print links[i].extract()

                item = self._inititem()

                location = links[i].xpath('h3/text()').extract()
                require = links[i].xpath('//div[@class="column"]/p[2]/text()').extract()
                work = links[i].xpath('//div[@class="column"]/p[1]/strong/a/text()').extract()
                deadline = links[i].xpath('//div[@class="column"]/p[3]/strong/text()').extract()
                applymethod = links[i].xpath('//div[@class="column"]/p[4]/text()').extract()


                if location:
                    item['location'] = StrUtil.delWhiteSpace(location[0])

                if require and (require != requireTemp):
                    item['require'] = StrUtil.delWhiteSpace(require[0])
                    requireTemp = require

                if work and (work != workTemp):
                    item['work'] = StrUtil.delWhiteSpace(work[0])
                    workTemp = work

                if deadline and (deadline != deadlineTemp):
                    item['deadline'] = StrUtil.delWhiteSpace(deadline[0])
                    deadlineTemp = deadline

                if applymethod and (applymethod != applymethodTemp):
                    item['applymethod'] = StrUtil.delWhiteSpace(applymethod[0])
                    applymethodTemp = applymethod

                logger.debug('>>>IGCEBjob>>>locaton>>>%s' % item["location"])
                logger.debug('>>>IGCEBjob>>>require>>>%s' % item["require"])
                logger.debug('>>>IGCEBjob>>>work>>>%s' % item["work"])
                logger.debug('>>>IGCEBjob>>>deadline>>>%s' % item["deadline"])
                logger.debug('>>>IGCEBjob>>>applymethod>>>%s' % item["applymethod"])

                yield item

    def _inititem(self):
        '''
        初始化全部字段
        :return:
        '''
        item = ICGEBjobDataItem()
        item['englishname'] = 'ICGEB'
        item['chinesename'] = '国际遗传工程和生物技术中心'
        item['incontinent'] = '欧洲'
        item['incountry'] = '意大利'
        item['type'] = '科学研究'
        item['url'] = 'http://www.icgeb.org/home-nd.html'
        item['alljoburl'] = 'http://www.icgeb.org/vacancies.html'
        item["location"] = ""
        item["require"] = ""
        item["work"] = ""
        item["deadline"] = ""
        item["applymethod"] = ""
        item["joburl"] = ""
        logger.info('初始化IDGEB工作和item成功')
        return item


