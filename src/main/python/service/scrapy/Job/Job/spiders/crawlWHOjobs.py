# -*- coding: utf-8 -*-
__author__ = 'liuyang'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import re
import json
import requests
from scrapy.http import Request
from ..allitems.jobitems import WHOjobDataItem
import logging.config
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

class WHOjobSpider(scrapy.Spider):
    name = "WHOjob"

    def __init__(self):
        logger.debug("开始爬取WHO岗位信息")
        self.preurl = "https://tl-ex.vcdp.who.int/careersection/ex/jobdetail.ftl?job="

    def start_requests(self):
        ur = 'https://tl-ex.vcdp.who.int/careersection/rest/jobboard/searchjobs?lang=en&portal=101430233'
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Content-Length": "946",
            "Content-Type": "application/json",
            "Cookie": "locale=en",
            "Host": "tl-ex.vcdp.who.int",
            "Origin": "https://tl-ex.vcdp.who.int",
            "Referer": "https://tl-ex.vcdp.who.int/careersection/ex/jobsearch.ftl",
            "tz": "GMT+08:00",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        data = json.loads('{"multilineEnabled":true,"sortingSelection":\
                {"sortBySelectionParam":"3","ascendingSortingOrder":"false"},\
                "fieldData":{"fields":{"KEYWORD":"","LOCATION":""},\
                "valid":true},"filterSelectionParam":{"searchFilterSelections":[{"id":"POSTING_DATE","selectedValues":[]},\
                {"id":"LOCATION","selectedValues":[]},\
                {"id":"JOB_FIELD","selectedValues":[]},\
                {"id":"JOB_TYPE","selectedValues":[]},\
                {"id":"JOB_SCHEDULE","selectedValues":[]},\
                {"id":"JOB_LEVEL","selectedValues":[]},\
                {"id":"EMPLOYEE_STATUS","selectedValues":[]}]},\
                "advancedSearchFiltersSelectionParam":{"searchFilterSelections":[{"id":"ORGANIZATION","selectedValues":[]},\
                {"id":"LOCATION","selectedValues":[]},\
                {"id":"JOB_FIELD","selectedValues":[]},\
                {"id":"JOB_NUMBER","selectedValues":[]},\
                {"id":"URGENT_JOB","selectedValues":[]},\
                {"id":"EMPLOYEE_STATUS","selectedValues":[]},\
                {"id":"JOB_SCHEDULE","selectedValues":[]},\
                {"id":"JOB_TYPE","selectedValues":[]},\
                {"id":"JOB_LEVEL","selectedValues":[]}]},"pageNo":2}')
        for i in range(1, 6, 1):
            data["pageNo"] = i
            post_data = json.dumps(data)
            response = requests.post(ur, data=post_data, headers=headers)
            result = json.loads(response.text)
            for everydata in result["requisitionList"]:
                work = everydata["column"][0]
                num = everydata["column"][1]
                Location = everydata["column"][2].strip('[').strip(']').strip('"')
                PostLevel = everydata["column"][3]
                ContractualArrangement = everydata["column"][4]
                ClosingDate = everydata["column"][5]
                yield Request(url=self.preurl + num,
                              callback=self.parseWHOjob,
                              meta={'work':work,
                                    'Location':Location,
                                    'PostLevel':PostLevel,
                                    'ContractualArrangement':ContractualArrangement,
                                    'ClosingDate':ClosingDate})

    def parseWHOjob(self,response):
        item = self.setitem(response)
        selector = scrapy.Selector(response)

        # 爬取合同期限
        ContractdurationXpath = '//div[@class="editablesection"]/div[@id="requisitionDescriptionInterface.ID1489.row1"]/' \
                                'span[@id="requisitionDescriptionInterface.ID1522.row1"]/text()'
        Contractduration = response.xpath(ContractdurationXpath).extract()
        item["Contractduration"] = Contractduration[0] if Contractduration else ""

        # 爬取主要地点
        PrimaryLocationXpath = '//div[@class="editablesection"]/div[@id="requisitionDescriptionInterface.ID1653.row1"]/' \
                               'span[@id="requisitionDescriptionInterface.ID1696.row1"]/text()'
        PrimaryLocation = response.xpath(PrimaryLocationXpath).extract()
        item["PrimaryLocation"] = PrimaryLocation[0] if Contractduration else ""

        # 爬取工作公告
        JobPostingXpath = '//div[@class="editablesection"]/div[@id="requisitionDescriptionInterface.ID1549.row1"]/' \
                          'span[@id="requisitionDescriptionInterface.reqPostingDate.row1"]/text()'
        JobPosting = response.xpath(JobPostingXpath).extract()
        item["JobPosting"] = JobPosting[0] if JobPosting else ""

        # 爬取所在组织
        OrganizationXpath = '//div[@class="editablesection"]/div[@id="requisitionDescriptionInterface.ID1753.row1"]/' \
                            'span[@id="requisitionDescriptionInterface.ID1796.row1"]/text()'
        Organization = response.xpath(OrganizationXpath).extract()
        item["Organization"] = Organization[0] if Organization else ""

        # 爬取是否要求全职
        ScheduleXpath = '//div[@class="editablesection"]/div[@id="requisitionDescriptionInterface.ID1803.row1"]/' \
                        'span[@id="requisitionDescriptionInterface.ID1846.row1"]/text()'
        Schedule = response.xpath(ScheduleXpath).extract()
        item["Schedule"] = Schedule[0] if Schedule else ""

        datas = response.xpath('//div[@class="editablesection"]').extract()
        data = "".join(datas)
        if re.search('REQUIRED QUALIFICATIONS', data) != None:
            first = re.search('REQUIRED QUALIFICATIONS', data).span()[1]
            end = re.search('REMUNERATION', data).span()[0]

            require = data[first:end]
            item["Required"] = require
        else:
            pass
        yield item

    def setitem(self,response):
        '''
        初始化WHO的item
        '''
        item = WHOjobDataItem()
        item["englishname"] = "WHO"
        item["chinesename"] = "世界卫生组织"
        item["incontinent"] = "欧洲"
        item["incountry"] = "瑞士"
        item["type"] = "卫生"
        item["url"] = "http://www.who.int/en/"
        item["alljoburl"] = "https://tl-ex.vcdp.who.int/careersection/ex/jobsearch.ftl#"
        item["joburl"] = response.url
        item["work"] = response.meta["work"]
        item["Location"] = response.meta["Location"]
        item["PostLevel"] = response.meta["PostLevel"]
        item["ContractualArrangement"] = response.meta["ContractualArrangement"]
        item['ClosingDate'] = response.meta["ClosingDate"]
        return item

