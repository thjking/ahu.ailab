# -*- coding: utf-8 -*-
__author__ = 'Liuyang'

import sys
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil
from src.main.python.dao.jobDao.CsvCao import SaveToCsv
from src.main.python.service.scrapy.Job.Job.utils.strUtil import StrUtil
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import re
import logging.config
logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')
WIPOPath = u"WIPO.csv"

class WIPOJobsSpider(object):

    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def start(self):

        self.driver.get('https://wipo.taleo.net/careersection/wp_2/jobsearch.ftl?lang=en#')
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        time.sleep(3)

        if 'Job' in self.driver.page_source:
            response = HtmlResponse(url="my HTML string", body=self.driver.page_source, encoding="utf-8")
            links = response.xpath('//div[@class="multiline-data-container"]/div/span/a/@href').extract()
            logger.info("WIPO共" + str(len(links)) + "条网页待爬")
            items = []
            for link in links:
                logger.debug("WIPO待爬岗位:  " + "https://wipo.taleo.net" + link)
                url = 'https://wipo.taleo.net' + link
                self.driver.get(url)
                time.sleep(3)
                item = self._parse(self.driver.page_source,url)
                if item not in items:
                    logger.debug("页面%s爬取成功"%url)
                    items.append(item)


            logger.debug("共爬取WIPO岗位数据%d条"%len(items))
            saveToCsv = SaveToCsv()
            saveToCsv.saveWIPOjobs(WIPOPath, items)
        else:
            self.start()

    def _parse(self,page_sourse,url):

        item = {}
        item["englishname"] = "WIPO"
        item["chinesename"] = "世界知识产权组织"
        item["incontinent"] = "欧洲"
        item["incountry"] = "瑞士"
        item["type"] = "知识产权"
        item["url"] = "http://www.wipo.int/portal/en/index.html"
        item["alljoburl"] = "https://wipo.taleo.net/careersection/wp_2/jobsearch.ftl?lang=en#"
        item["joburl"] = url

        response = HtmlResponse(url="my HTML string", body=page_sourse, encoding="utf-8")

        workinfo = response.xpath('//div[@class="editablesection"]/div[1]')
        work = workinfo.xpath('string(.)').extract()[0]
        item["work"] = re.sub('\W','',work.split('-')[0])  # 岗位

        sectorinfo = response.xpath('//div[@class="editablesection"]/div[2]')
        sector = sectorinfo.xpath('string(.)').extract()[0]
        item["sector"] = sector        # 部门

        gradeinfo = response.xpath('//div[@class="editablesection"]/div[3]')
        grade = gradeinfo.xpath('string(.)').extract()[0]
        item["grade"] = re.sub('\W','',grade.split('-')[1])        # 职级

        contractinfo = response.xpath('//div[@class="editablesection"]/div[4]')
        contract = contractinfo.xpath('string(.)').extract()[0]
        item["ContractDuration"] = re.sub('\W','',contract.split('-')[-1])        # 合同期限

        DutyStationinfo = response.xpath('//div[@class="editablesection"]/div[5]')
        DutyStation = DutyStationinfo.xpath('string(.)').extract()[0]
        item["DutyStation"] = re.sub('\W','',DutyStation.split(':')[-1])        # 工作地点

        timeinfo = response.xpath('//div[@class="editablesection"]/div[6]')
        time = timeinfo.xpath('string(.)').extract()[0]        # 时间

        item["PublicationDate"] = re.sub('\W','',time.split('Application Deadline')[0].split(':')[-1])       # 发起时间

        item["ApplicationDeadline"] = re.sub('\W','',time.split('Application Deadline')[-1])        # 截止时间

        requireinfo = response.xpath('//div[@class="editablesection"]/div[7]')
        require = re.sub('\n',' ',requireinfo.xpath('string(.)').extract()[0])

        item["Organizationalcontext"] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(require.split('Organizational context')[-1].split
                                                                                   ('Duties and responsibilities')[0]))        # 组织背景

        item["Dutiesandresponsibilities"] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(require.split('Organizational context')[-1].split
                                            ('Duties and responsibilities')[-1].split('Requirements')[0]))        # 责任与义务

        item["Requirements"] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(require.split('Organizational context')[-1].split
                    ('Duties and responsibilities')[-1].split('Requirements')[-1].split('Organizational competencies')[0]))        # 要求

        item["Organizationalcompetencies"] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(require.split('Organizational context')[-1].split
        ('Duties and responsibilities')[-1].split('Requirements')[-1].split('Organizational competencies')[-1].split('Information')[0]))        # 组织能力

        item["Information"] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(require.split('Organizational context')[-1].split
        ('Duties and responsibilities')[-1].split('Requirements')[-1].split('Organizational competencies')[-1].split('Information')[-1]))        # 相关信息

        return item

    def depose(self):
        self.driver.close()

if __name__ == "__main__":
    wIPOJobsSpider = WIPOJobsSpider()
    wIPOJobsSpider.start()
    wIPOJobsSpider.depose()
