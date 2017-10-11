# -*- coding: utf-8 -*-
__author__ = 'Robin'

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from scrapy import signals
try:
    from pydispatch import dispatcher
except:
    from scrapy.xlib.pydispatch import dispatcher
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil
import logging.config
from scrapy.http import Request
from ..allitems.jobitems import CERNjobDataItem

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

class CERNjobsSpider(scrapy.Spider):
    name = 'CERNjobs'
    start_urls = [
        'http://jobs.web.cern.ch/latest-jobs?page=0',
        'http://jobs.web.cern.ch/latest-jobs?page=1']
    
    def __init__(self):
        logger.debug('开始爬取CERN岗位信息')
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        selector = scrapy.Selector(response)
        links = selector.xpath("//table[@class='views-view-grid cols-1']/tbody/tr/td/div[1]/span/a/@href").extract()
        for link in links:
            logger.debug('开始爬取%s' % link)
            yield Request(url=link, callback=self.parseDetials)

    def parseDetials(self, response):
        item = self._initItem()
        selector = scrapy.Selector(response)
        # print 'selector is ', selector
        item['joburl'] = response.url
        con = selector.xpath("//div[@class='views-row views-row-1 views-row-odd views-row-first views-row-last']")
        item['Jobtitle'] = ' '.join(con[0].xpath("div[@class='views-field views-field-title']/span/h1/text()").extract())
        item['Jobdescription'] = ' '.join(con[0].xpath("div[@class='views-field views-field-field-job-descr']/div/p/text()").extract())
        item['Jobreference'] = ' '.join(con[0].xpath("span[@class='views-field views-field-field-job-ref']/span[@class='field-content']/text()").extract())
        item['Publicationdate'] = ' '.join(con[0].xpath("div[@class='views-field views-field-field-job-pub-date']/div/span/text()").extract())
        item['closingdate'] = ' '.join(con[0].xpath("div[@class='views-field views-field-field-job-date-closed']/div/span/text()").extract())
        item['Introduction'] = ' '.join(con[0].xpath("div[@class='views-field views-field-field-job-intro-en']/div//p/text()").extract())
        item['Functions'] = ' '.join(con[0].xpath("div[@class='views-field views-field-field-job-function-en']/div/ul//li/text()").extract())
        item['QualificationRequired'] = ' '.join(con[0].xpath("div[@class='views-field views-field-field-job-qualification-en']/div//p/text()").extract())
        item['ExperienceandCompetencies'] = ' '.join(con[0].xpath("div[@class='views-field views-field-field-job-experience-en']/div/text()").extract())
        item['EligibilityConditions'] = ' '.join(con[0].xpath("div[@class='views-field views-field-field-job-eligibility-en']/div//p/text()").extract())
        item['NoteonEmploymentConditions'] = ' '.join(con[0].xpath("div[@class='views-field views-field-field-job-empl-cond-en']/div/text()").extract())
        yield item
    
    def _initItem(self):
        item = CERNjobDataItem()
        item['englishname'] = 'CERN'
        item['chinesename'] = '欧洲核子研究组织'
        item['incontinent'] = '欧洲'
        item['incountry'] = '瑞士'
        item['type'] = '物理'
        item['url'] = 'https://home.cern/'
        item['alljoburl'] = 'http://jobs.web.cern.ch/latest-jobs'
        item['joburl'] = ''
        item['Jobdescription'] = ''
        item['Jobreference'] = ''
        item['Publicationdate'] = ''
        item['closingdate'] = ''
        item['Introduction'] = ''
        item['Functions'] = ''
        item['QualificationRequired'] = ''
        item['ExperienceandCompetencies'] = ''
        item['EligibilityConditions'] = ''
        item['NoteonEmploymentConditions'] = ''
        return item

    
    def spider_closed(self):
        logger.info('已爬取%d个岗位' % len(self.items))
