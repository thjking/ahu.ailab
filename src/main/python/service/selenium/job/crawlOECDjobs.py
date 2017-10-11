# -*- coding: utf-8 -*-

__author__ = 'Liuyang'

import sys
sys.path.append('/home/robin/Workspace/pycode/venv/JobSpider/ahu.ailab')
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
OECDJobsPath = u"OECD.csv"

class OECDJobSpider(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def start(self):
        items = []
        retrynum = 0
        self.driver.get("https://oecd.taleo.net/careersection/ext/joblist.ftl")
        time.sleep(20)
        # self.driver.maximize_window()
        self.driver.implicitly_wait(30)

        # 判断页面是否加载成功
        if "Job" in self.driver.page_source:
            # 进入第一个职位
            click_text = u"Health Policy Analysts"
            self.driver.find_element_by_partial_link_text(click_text).click()
            item = self.pars(self.driver.page_source)
            items.append(item)
            time.sleep(3)
            for i in range(0,23,1):
                if "Job" in self.driver.page_source:
                    self.driver.find_element_by_partial_link_text("Next").click()
                    time.sleep(3)
                    item = self.pars(self.driver.page_source)
                    if item not in items:
                        items.append(item)
                        logger.debug('爬取岗位%s成功'%item['work'])
                else:
                    logger.error("页面加载失败")
        else:
            retrynum += 1
            time.sleep(5)
            if retrynum < 10:
                self.driver.refresh()
                self.start()

        # TODO 保存爬取的数据
        logger.info("OECDJob>>>共爬取岗位数%d"%len(items))
        saveToCsv = SaveToCsv()
        saveToCsv.saveOECDjobs(OECDJobsPath,items)

    def pars(self,page_sourse):

        item = {}
        response = HtmlResponse(url="my HTML string", body=page_sourse, encoding="utf-8")
        item["englishname"] = "OECD"
        item["chinesename"] = "经济合作与发展组织"
        item["incontinent"] = "欧洲"
        item["incountry"] = "法国"
        item["type"] = "经济"
        item["url"] = "http://www.oecd.org/"
        item["alljoburl"] = "https://oecd.taleo.net/careersection/ext/joblist.ftl"
        item['Description'] = ''
        item['MainResponsibilities'] = ''
        item["IdealCandidateProfile"] = ''
        item["Contract"] = ''
        item["offers"] = ''

        # 岗位名称
        workdata = response.xpath('//div[@class="editablesection"]/div[1]')
        workinfo = workdata.xpath('string(.)').extract()
        item["work"] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(workinfo[0]))

        # 其他岗位信息
        otherdata = response.xpath('//span[@id="requisitionDescriptionInterface.ID1451.row1"]')
        require =   re.sub('\n',' ',otherdata.xpath('string(.)').extract()[0])

        info1 = require.split('Main')
        for i in info1[:-1]:
            item['Description'] += i
        item['Description'] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(item['Description']))

        info2 = info1[-1].split('Ideal')
        for i in info2[:-1]:
            item['MainResponsibilities'] += i
        item['MainResponsibilities'] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(item['MainResponsibilities']))

        info3 = info2[-1].split('Contract')
        for i in info3[:-1]:
            item["IdealCandidateProfile"] += i
        item["IdealCandidateProfile"] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(item["IdealCandidateProfile"]))

        if 'What the OECD offers' in info3[-1]:
            info4 = info3[-1].split('What the OECD offers')
            item["Contract"] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(info4[0]))
            item["offers"] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(info4[1]))
        else:
            item["Contract"] = StrUtil.delMoreSpace(StrUtil.delWhiteSpace(info3[-1]))
        return item

    def depose(self):
        self.driver.close()


if __name__ == "__main__":
    oECDJobSpider = OECDJobSpider()
    oECDJobSpider.start()
    oECDJobSpider.depose()
    