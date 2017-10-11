# -*- coding: utf-8 -*-
__author__ = 'chenjailin'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from scrapy.http import Request
from ..allitems.jobitems import UNUjobDataItem
from src.main.python.service.scrapy.Job.Job.utils.strUtil import StrUtil
import logging.config
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

class UNUjobSpider(scrapy.Spider):
    name = "UNUjob"

    start_urls = ["https://unu.edu/admissions/doctoral",
                  "https://unu.edu/admissions/masters",
                  "https://unu.edu/admissions/non-degree"]

    def __init__(self):
        logger.debug("开始爬取UNU招聘信息")

    def parse(self, response):
        selector = scrapy.Selector(response)

        jobs = selector.xpath('//article[@class="list-item"]/div/h4/a')
        i=0
        for job in jobs:
            i += 1
            try:
                url = job.xpath('@href').extract()[0]
                logger.debug("开始爬取第%d个职位" % i)
                yield Request(url=url,callback=self._parseUNUjob)
            except:
                pass
        logger.info("共爬取%d个招聘信息"%i)


    def _parseUNUjob(self, response):
        selector = scrapy.Selector(response)
        item = self._inititem()
        item['joburl'] = response.url
        describe = selector.xpath('//li[@id="overview_tab"]/div/p/text()').extract()
        if describe:
            res = ''
            for text in describe:
                res += text
            item["describe"] = StrUtil.delWhiteSpace(res)
            logger.debug('>>UNU>>job>>describe>>%s' % item["describe"])
        else:
            logger.error('爬取岗位描述失败，网页结构可能改变，建议检查')

        try:
            Title = selector.xpath('//section[@class="eight phone-four columns "]/h1/text()').extract()[0]
            item['Title'] = StrUtil.delWhiteSpace(Title)
            logger.debug('>>UNU>>job>>Title>>%s' % item["Title"])
        except:
            pass

        try:
            recruitment = selector.xpath('//li[@id="contact_tab"]/div/p/descendant::text()').extract()
            res = ''
            for text in recruitment:
                res += text
            item['recruitment'] = StrUtil.delWhiteSpace(res)
            logger.debug('>>UNU>>job>>recruitment>>%s' % item["recruitment"])
        except:
            pass

        info = selector.xpath('//dl[@class="summary mar-b-10"]/dd/text()').extract()
        applytime = info[2]
        if applytime:
            item['applytime'] = StrUtil.delWhiteSpace(applytime)
            logger.debug('>>UNU>>job>>applytime>>%s' % item["applytime"])
        else:
            logger.error('爬取申请截止时间失败，网页结构可能改变，建议检查')

        starting_date = info[0]
        if starting_date:
            item['starting_date'] = StrUtil.delWhiteSpace(starting_date)
            logger.debug('>>UNU>>job>>starting_date>>%s' % item["starting_date"])
        else:
            logger.error('爬取开始日期失败，网页结构可能改变，建议检查')

        location = info[1]
        if location:
            item['location'] = StrUtil.delWhiteSpace(location)
            logger.debug('>>UNU>>job>>location>>%s' % item["location"])
        else:
            logger.error('爬取开设国家失败，网页结构可能改变，建议检查')

        try:
            application = selector.xpath('//li[@id="application_precedure_tab"]/div/p')
            joburl = application.xpath('a/@href').extract()[0]
            item['outurl'] = StrUtil.delWhiteSpace(joburl)
            logger.debug('>>UNU>>job>>outurl>>%s' % item["outurl"])

            application_procedure = application.xpath('string(.)').extract()[0]

            item['application_procedure'] = StrUtil.delWhiteSpace(application_procedure)
            logger.debug('>>UNU>>job>>application_procedure>>%s' % item["application_procedure"])
        except:
            pass

        yield item

    def _inititem(self):
        item = UNUjobDataItem()
        item['englishname'] = 'UNU'
        item['chinesename'] = '联合国大学'
        item['incountry'] = '日本'
        item['incontinent'] = '亚洲'
        item['type'] = '科学研究'
        item['url'] = 'unu.edu'
        item['alljoburl'] = 'https://unu.edu/admissions'
        item['describe'] = ''
        item['Title'] = ''
        item['recruitment'] = ''
        item['applytime'] = ''
        item['starting_date'] = ''
        item['location'] = ''
        item['outurl'] = ''
        item['application_procedure'] = ''
        logger.info('初始化job item成功')
        return item