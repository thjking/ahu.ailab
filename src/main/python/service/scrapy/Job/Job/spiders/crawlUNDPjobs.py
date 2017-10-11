# -*- coding: utf-8 -*-
__author__ = 'liuyang'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import re
from scrapy.http import Request
from ..allitems.jobitems import UNDPJobDataItem,UNDPJobDataItem2
from src.main.python.service.scrapy.Job.Job.utils.strUtil import StrUtil
import logging.config
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

class UNDPjobSpider(scrapy.Spider):

    name = "UNDPjob"

    start_urls = ["https://jobs.undp.org/cj_view_jobs.cfm"]

    def __init__(self):
    
        self.noidziduan = ['Location :','Application Deadline :','Additional  Category :',
                       'Type of Contract :','Post Level :','Languages Required :','Duration of Initial Contract :',
                       'Expected Duration of Assignment :']

        self.ITE = ['Location','ApplicationDeadline','TypeofContract','PostLevel','LanguagesRequired',
                    'DurationofInitialContract','ExpectedDurationofAssignment','AdditionalCategory']

        self.textnfo_noid = ['Background','Duties and Responsibilities','Competencies','Required Skills and Experience']

        self.id2field = ['Agency', 'Title', 'Job ID', 'Practice Area - Job Family', 'Vacancy End Date', 'Time Left', 
                        'Duty Station', 'Education & Work Experience', 'Languages', 'Grade', 'Vacancy Type', 'Posting Type',
                        'Bureau', 'Contract Duration', 'Background', 'Duties and Responsibilities', 'Competencies', 'Required Skills and Experience', 
                        'Disclaimer']

        self.preurl = "https://jobs.undp.org/"

        # 用来存储第二种页面信息的容器
        self.items = []

    def parse(self, response):
        selector = scrapy.Selector(response)
        logger.debug("开始解析UNDP(联合国开发计划蜀)的连接信息")
        table = selector.xpath('//div[@id="content-main"]/table[@class="table-sortable"]')
        for evertable in table:
            tbody = evertable.xpath('tr')
            for everlink in tbody[:-1]:
                # 提取具体岗位连接
                link = everlink.xpath('td[1]/a/@href').extract()
                if len(link):
                    if link[0].startswith('c'):
                        LINK = self.preurl + link[0]
                    else:
                        LINK = link[0]
                else:
                    continue
                # print LINK

                # 提取岗位描述信息
                describe = everlink.xpath('td[1]/a/text()').extract()
                DESERIBE = describe[0] if len(describe) else ""
                # print DESERIBE

                # 提取所属系统(第二列)
                suoshu = everlink.xpath('td[2]/text()').extract()
                SUOSHU = suoshu[0] if len(suoshu) else ""
                # print SUOSHU

                # 提取岗位名称
                work = everlink.xpath('td[3]/text()').extract()
                WORK = work[0].strip() if len(work) else ""
                # print WORK

                # 提取岗位申请时间
                applytime = everlink.xpath('td[4]/text()').extract()
                APPLYTIME = applytime[1] if len(applytime) else ""
                # print APPLYTIME

                # 提取岗位联系人
                linkman = everlink.xpath('td[5]/text()').extract()
                LINKMAN = linkman[0] if len(linkman) else ""
                # print LINKMAN

                if LINK.endswith('id=2'):
                    logger.debug("开始爬取链接%s"%LINK)
                    yield Request(url=LINK,
                                    callback=self._crawlhaveid,
                                    meta={"describe":DESERIBE,
                                            "suoshu":SUOSHU,
                                            "applytime":APPLYTIME,
                                            "linkman":LINKMAN})

                else:
                    logger.debug("开始爬取链接%s" % LINK)
                    yield Request(url=LINK,
                                    callback=self._UNDPprase,
                                    meta={"describe":DESERIBE,
                                                "suoshu":SUOSHU,
                                                "work":WORK,
                                                "applytime":APPLYTIME,
                                                "linkman":LINKMAN}
                                          )

    def _UNDPprase(self, response):
        '''
       使用scrapy框架解析岗位信息（第一种页面形式）
       '''
        logger.debug('crawl noid!') 
        work_or_PostLevel = response.meta["work"]

        job = scrapy.Selector(response)
        item = self._setitem_noid(response)

        try:
            self._crawlnoid(job,item,work_or_PostLevel)
        except:
            logger.warning("未能爬取到页面%s的相关数据"%response.url)
        yield item

    def _crawlnoid(self,job,item,work_or_PostLevel):
    
        '''
        对第一种形式页面进行字段解析
        '''

        item["work"] = work_or_PostLevel
        #TODO  提取基本信息
        trs = job.xpath('//div[@id="content-main"]/table[1]/tr')

        for tr in trs:
            ziduanming = tr.xpath('td[1]/strong/text()').extract()
            if ziduanming:
                if ziduanming[0] in self.noidziduan:
                    context = tr.xpath('td[2]/text()').extract()
                    if context:
                        if StrUtil.delWhite(ziduanming[0].strip(':')) == "LanguagesRequired":
                            item[StrUtil.delWhite(ziduanming[0].strip(':'))] = re.sub('\W',' ',StrUtil.delWhite(context[0]))
                        else:
                            item[StrUtil.delWhite(ziduanming[0].strip(':'))] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(context[0]))


        # TODO  提取技能经历等数据
        skilldatas = job.xpath('//div[@id="content-main"]/table[2]/tr')

        for i in range(0,len(skilldatas),1):
            name = skilldatas[i].xpath('td[@class="field"]/h5/text()').extract()
            if name:
                if name[0] in self.textnfo_noid:
                    data = skilldatas[i+1].xpath('td[@class="text"]')
                    info = data.xpath('string(.)').extract()
                    item[StrUtil.delWhite(name[0])] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(info[0]))


    def _crawlhaveid(self,response):
        '''
        打开第二种形式页面并进行页面提取
        '''
        item = self.setitem_haveid(response)
        item['joburl'] = response.url

        try:
            self.crawlinfohaveid(item,response)
        except:
            logger.error("crawl failed!")
        yield item

    def crawlinfohaveid(self, item, response):

        '''
        对第二种页面进行字段提取
        '''
        logger.debug('crawl haveid!')

        selector = scrapy.Selector(response)
        table = selector.xpath("//table[@id='ACE_$ICField30$0']/tbody/tr/td")
        tds = [t.strip() for t in table.xpath("string(.)").extract()]

        table2 = selector.xpath("//table[@id='ACE_HRS_JO_PST_DSCR$0']/tbody/tr/td")
        tds2 = [t.strip() for t in table2.xpath("string(.)").extract()]
        tds.extend(tds2)
        tds.append('Disclaimer')
        temp = []
        key = 'default'
        value = ''

        try:
            for td in tds:
                # if td:
                    # print td
                if td in self.id2field:
                    value = StrUtil.delMoreSpace(''.join(temp).encode('utf-8'))
                    try:
                        item[key] = value
                    except:
                        pass
                    temp = []
                    key = re.sub('[-& ]', '', td.encode('utf-8'))
                else:
                    temp.append(td)

            self.items.append(item)
        except:
            logger.error('parser error!')
        

    def setitem_haveid(self,response):
        '''
        初始化第二种页面全部字段
        '''
        item = UNDPJobDataItem2()
        item["englishname"] = "UNDP"
        item["chinesename"] = "联合国开发计划署"
        item["incontinent"] = "北美洲"
        item["incountry"] = "美国"
        item["type"] = "科学研究"
        item["url"] = "http://www.undp.org/"
        item["alljoburl"] = "https://jobs.undp.org/cj_view_jobs.cfm"
        item["joburl"] = response.url
        item["describe"] = response.meta["describe"]
        item["suoshu"] = response.meta["suoshu"]
        item["applytime"] = response.meta["applytime"]
        item["linkman"] = response.meta["linkman"]
        return item

    def _setitem_noid(self,response):
        '''
        初始化第一种页面全部字段
        '''
        item = UNDPJobDataItem()
        item["work"] = ""
        item["englishname"] = "UNDP"
        item["chinesename"] = "联合国开发计划署"
        item["incontinent"] = "北美洲"
        item["incountry"] = "美国"
        item["type"] = "科学研究"
        item["url"] = "http://www.undp.org/"
        item["alljoburl"] = "https://jobs.undp.org/cj_view_jobs.cfm"
        item["joburl"] = response.url
        item["describe"] = response.meta["describe"]
        item["suoshu"] = response.meta["suoshu"]
        item["applytime"] = response.meta["applytime"]
        item["linkman"] = response.meta["linkman"]
        for ite in self.ITE:
            item[ite] = ""
        return item