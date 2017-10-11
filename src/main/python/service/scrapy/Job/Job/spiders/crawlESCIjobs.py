# -*- coding: utf-8 -*-
__author__ = 'Robin'

import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from scrapy import signals
try:
    from pydispatch import dispatcher
except:
    from scrapy.xlib.pydispatch import dispatcher
from bs4 import BeautifulSoup
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil
import logging.config
from scrapy.http import Request

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')
path = u"ESCI.csv"

class ESCIjobsSpider(scrapy.Spider):

    name = 'ESCIjobs'

    start_urls = ['https://escience.org.cn/International/position/search?page=0&job=',
                  'https://escience.org.cn/International/position/search?page=1&job=']

    def __init__(self):
        logger.debug('开始爬取escience岗位信息')
        self.url = 'https://escience.org.cn'
        self.items = []
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        selector = scrapy.Selector(response)
        pattern = re.compile(r".*page=([0-9]*)&.*")
        id = re.match(pattern, response.url).group(1)
        # if not eval(id):
            # L = selector.xpath("//ul[@class='pagination']/li")
            # print L
            # self.addurls(len(L)-2)
        trs = selector.xpath("//tbody[@id='position-list']/tr")
        logger.info('开始爬取第%d页%d个岗位' % (eval(id)+1, len(trs)))
        for t in trs:
            item = {}
            self._initItem(item)
            tds = t.xpath('td')
            # print len(tds)
            # print tds[0]
            link = tds[0].xpath("a/@href").extract()[0]
            item['jobname'] = tds[0].xpath('a/text()').extract()[0]
            # print item['jobname']
            item['joburl'] = response.url
            item['companyname'] = tds[1].xpath('text()').extract()[0]
            item['position'] = tds[2].xpath('text()').extract()[0]
            item['date'] = tds[3].xpath('text()').extract()[0]
            # print item['companyname']
            if item['companyname'] == '欧洲核子研究组织':
                yield Request(url=self.url+link, callback=self.parseCERN, meta={
                    'item': item
                })
            elif item['companyname'] == '联合国大学':
                yield Request(url=self.url+link, callback=self.parseUNU, meta={
                    'item': item
                })
            elif item['companyname'] == '国际热核聚变实验堆计划':
                yield Request(url=self.url+link, callback=self.parseITER, 
                meta={
                    'item': item
                })
        # logger.info('爬取%d个岗位完成' % len(self.items))

    # def addurls(self, length):
    #     # print length
    #     for i in range(1, length):
    #         url = 'https://escience.org.cn/International/position/search?page=' + str(i) + '&job='
    #         # print 'next url is ' + url
    #         start_urls.append(url)

    def parseCERN(self, response):
        # print 'CERN'
        item = response.meta['item']
        # print item['jobname']
        selector = scrapy.Selector(response)
        con = selector.xpath("//div[@class='views-row views-row-1 views-row-odd views-row-first views-row-last']")
        item['Job description'] = " ".join(con[0].xpath("div[@class='views-field views-field-field-job-descr']/div/p/text()").extract())
        item['Job reference'] = " ".join(con[0].xpath("span[@class='views-field views-field-field-job-ref']/span[@class='field-content']/text()").extract())
        item['Publication date'] = " ".join(con[0].xpath("div[@class='views-field views-field-field-job-pub-date']/div/span/text()").extract())
        item['closing date'] = " ".join(con[0].xpath("div[@class='views-field views-field-field-job-date-closed']/div/span/text()").extract())
        item['Introduction'] = " ".join(con[0].xpath("div[@class='views-field views-field-field-job-intro-en']/div//p/text()").extract())
        item['Functions'] = " ".join(con[0].xpath("div[@class='views-field views-field-field-job-function-en']/div/ul//li/text()").extract())
        item['Qualification required'] = " ".join(con[0].xpath("div[@class='views-field views-field-field-job-qualification-en']/div//p/text()").extract())
        item['Experience and competencies'] =  " ".join(con[0].xpath("div[@class='views-field views-field-field-job-experience-en']/div/text()").extract())
        item['Eligibility conditions'] = " ".join(con[0].xpath("div[@class='views-field views-field-field-job-eligibility-en']/div//p/text()").extract())
        item['Note on Employment Conditions'] = " ".join(con[0].xpath("div[@class='views-field views-field-field-job-empl-cond-en']/div/text()").extract())
        # print item['Job description']
        # print item['Job reference']
        # print item['Publication date']
        # print item['closing date']
        # print item['Introduction']
        # print item['Functions']
        # print item['Qualification required']
        # print item['Experience and competencies']
        # print item['Eligibility conditions']
        # print item['Note on Employment Conditions']
        self.items.append(item)

    def parseITER(self, response):
        # print 'ITER'
        item = response.meta['item']
        # print response.text
        soup = BeautifulSoup(response.text, 'html.parser')
        # print soup
        trs = soup.find('div', class_='col-sm-12').find('table').find('tbody').find_all('tr')  
        # print trs
        for t in trs:
            try:
                # print t
                td = t.find_all('td')
                # print td[0].find('span').text
                key = td[0].find('div').find('span').text
                value = td[1].find('span').text
                item[key] = value
                # print key, '=>', value
            except:
                pass
        self.items.append(item)



    def parseUNU(self, response):
        # print 'UNU'
        item = response.meta['item']
        selector = scrapy.Selector(response)
        dds = selector.xpath("//div[@class='col-sm-12']/li[@id='overview_tab']/div[@class='page_contents']/dl//dd")
        item['POSITION'] = dds[0].xpath('string(.)').extract()[0]
        item['REFERENCE NO.'] = dds[1].xpath('text()').extract()[0]
        item['LOCATION'] = dds[2].xpath('text()').extract()[0]
        item['Timezone'] = dds[3].xpath('text()').extract()[0]
        item['CLOSING DATE'] = dds[4].xpath('text()').extract()[0]
        # print item['POSITION']
        # print item['REFERENCE NO.']
        # print item['LOCATION']
        # print item['Timezone']
        # print item['CLOSING DATE']
        # print '\n'
        children = selector.xpath("//div[@class='col-sm-12']/li[@id='overview_tab']/div[@class='page_contents']/child::node()")
        pattern = re.compile('<h3>.*</h3>')
        key = 'default'
        value = ''
        # print len(children.extract())
        temp = []
        for kid in children:
            # print 'kid is ', kid.extract()
            ans = re.match(pattern, kid.extract())
            # print 'ans is ', ans
            if ans:
                # print 'key is', key
                value = ' '.join(temp)
                item[key] = value
                temp = []
                # print key, '=>', value                        
                key = kid.xpath('string(.)').extract()[0]
            else:
                try:
                    val = kid.xpath('string(.)').extract()[0]
                    # print 'value is', value
                    temp.append(val)
                except:
                    pass
        self.items.append(item)


    
    def _initItem(self, item):
        item = {}
        item['Job description'] = ""
        item['Job reference'] = ""
        item['Publication date'] = ""
        item['closing date'] = ""
        item['Introduction'] = ""
        item['Functions'] = ""
        item['Qualification required'] = ""
        item['Experience and competencies'] = ""
        item['Eligibility conditions'] = ""
        item['Note on Employment Conditions'] = ""
        
        item['Division'] = ""
        item['Diploma'] = ""
        item['Others'] = ""

        item['POSITION'] = ""
        item['REFERENCE NO.'] = ""
        item['LOCATION'] = ""
        item['Timezone'] = ""
        item['CLOSING DATE'] = ""
        item['United Nations University objectives'] = ""
        item['UNU Vice-Rectorate in Europe (UNU-ViE)'] = ""
        item['UNU Computing and Society (UNU-CS)'] = ""
        item['UNU Institute for Environment and Human Security (UNU-EHS)'] = ""
        item['Responsibilities'] = ""
        item['Main duties and responsibilities'] = ""
        item['Required qualifications and competencies'] = ""
        item['Remuneration'] = ""
        item['Duration of contract'] = ""
        item['Starting date'] = ""
        item['context'] = ""
        item['Job summary'] = ""

    def spider_closed(self):
        logger.info('共爬取%d个岗位' % len(self.items))
