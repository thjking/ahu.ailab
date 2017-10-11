# -*- coding: utf-8 -*-
# writen by Jing

import sys
sys.path.append('/home/robin/Workspace/pycode/venv/JobSpider/ahu.ailab')
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil
from src.main.python.dao.jobDao.CsvCao import SaveToCsv
from src.main.python.service.scrapy.Job.Job.utils.strUtil import StrUtil
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import logging.config
logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')
UNESCOJobsPath = u"UNESCO.csv"

class UNESCOJobSpider(object):

    def __init__(self):
        self.driver = webdriver.PhantomJS()


    def start(self):
        items = []
        retryum = 0
        self.driver.get("https://careers.unesco.org/careersection/1/joblist.ftl?lang=en")
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)

        # 判断页面是否加载成功
        if "Job" in self.driver.page_source:
            # 进入第一个职位
            click_text = u"EDITOR (ARABIC)"
            self.driver.find_element_by_partial_link_text(click_text).click()
            item = self.pars(self.driver.page_source)
            items.append(item)
            time.sleep(3)
            for i in range(0,23,1):
                if "Job" in self.driver.page_source:
                    self.driver.find_element_by_link_text("Next").click()
                    time.sleep(3)
                    item = self.pars(self.driver.page_source)
                    if item not in items:
                        items.append(item)
                        logger.debug('爬取岗位%s成功'%item['work'])
                else:
                        logger.debug("页面加载失败")
        else:
            retryum += 1
            time.sleep(5)
            if retryum < 10:
                self.driver.refresh()
                self.start()
        # Todo 保存爬取的数据
        logger.info("UNESCO>>共爬取岗位数%d"%len(items))
        saveToCSV = SaveToCsv()
        saveToCSV.saveUNESCOjobs(UNESCOJobsPath,items)

    def pars(self,page_sourse):

        item = {}
        response = HtmlResponse(url="my HTML string",body=page_sourse,encoding="utf-8")
        item["work"] = ""  # 位置
        item["domain"] = ""  # 领域
        item["postNumber"] = ""  # 邮政编号
        item["grade"] = ""  # 等级
        item["organizationalUnit"] = ""  # 组织单位
        item["primaryLocation"] = ""  # 主要位置
        item["recruitmentOpenTo"] = ""  # 招聘人员
        item["typeOfContract"] = ""  # 合同类型
        item["salary"] = ""  # 工资
        item["deadline"] = ""  # 截止日期
        item["functions"] = ""  # 功能
        item["qualifications"] = ""  # 要求

        # 岗位名称
        workdata = response.xpath('//div[@class="editablesection"]/div[1]/span[@class="titlepage"]')
        workinfo = workdata.xpath('string(.)').extract()
        print workinfo
        item["work"] = StrUtil.delWhiteSpace(StrUtil.delWhiteSpace(workinfo[1]))


        #其他岗位信息
        domaindata = response.xpath('//div[@class="editablesection"]/div[2]/span[@class="text"]')
        domaininfo = domaindata.xpath('string(.)').extract()
        print domaininfo
        item["domain"] = StrUtil.delWhiteSpace(StrUtil.delWhiteSpace(domaininfo[0]))

        postNumberdata = response.xpath('//div[@class="editablesection"]/div[3]/span[@class="text"]')
        postNumberinfo = postNumberdata.xpath('string(.)').extract()
        print postNumberinfo
        item["postNumber"] = StrUtil.delWhiteSpace(StrUtil.delWhiteSpace(postNumberinfo[0]))

        gradedata = response.xpath('//div[@class="editablesection"]/div[4]/span[@class="text"]')
        gradeinfo = gradedata.xpath('string(.)').extract()
        print gradeinfo
        item["grade"] = StrUtil.delWhiteSpace(StrUtil.delWhiteSpace(gradeinfo[0]))

        organizationalUnitdata = response.xpath('//div[@class="editablesection"]/div[5]/span[@class="text"]')
        organizationalUnitinfo = organizationalUnitdata.xpath('string(.)').extract()
        print organizationalUnitinfo
        item["organizationalUnit"] = StrUtil.delWhiteSpace(StrUtil.delWhiteSpace(organizationalUnitinfo[0]))

        primaryLocationdata = response.xpath('//div[@class="editablesection"]/div[6]/span[@class="text"]')
        primaryLocationinfo = primaryLocationdata.xpath('string(.)').extract()
        print primaryLocationinfo
        item["primaryLocation"] = StrUtil.delWhiteSpace(StrUtil.delWhiteSpace(primaryLocationinfo[0]))

        recruitmentOpenTodata = response.xpath('//div[@class="editablesection"]/div[7]/span[@class="text"]')
        recruitmentOpenToinfo = recruitmentOpenTodata.xpath('string(.)').extract()
        print recruitmentOpenToinfo
        item["recruitmentOpenTo"] = StrUtil.delWhiteSpace(StrUtil.delWhiteSpace(recruitmentOpenToinfo[0]))

        typeOfContractdata = response.xpath('//div[@class="editablesection"]/div[8]/span[@class="text"]')
        typeOfContractinfo = typeOfContractdata.xpath('string(.)').extract()
        print typeOfContractinfo
        item["typeOfContract"] = StrUtil.delWhiteSpace(StrUtil.delWhiteSpace(typeOfContractinfo[0]))

        salarydata = response.xpath('//div[@class="editablesection"]/div[10]/span[@class="text"]')
        salaryinfo = salarydata.xpath('string(.)').extract()
        print salaryinfo
        item["salary"] = StrUtil.delWhiteSpace(StrUtil.delWhiteSpace(salaryinfo[0]))

        deadlinedata = response.xpath('//div[@class="editablesection"]/div[12]/span[@class="text"]')
        deadlineinfo = deadlinedata.xpath('string(.)').extract()
        print deadlineinfo
        item["deadline"] = StrUtil.delWhiteSpace(StrUtil.delWhiteSpace(deadlineinfo[0]))

        functionsdata = response.xpath('//div[@class="editablesection"]/div[16]')
        functionsinfo = functionsdata.xpath('string(.)').extract()
        print functionsinfo
        item["functions"] = StrUtil.delWhiteSpace(StrUtil.delWhiteSpace(functionsinfo[0]))

        qualificationsdata = response.xpath('//div[@class="editablesection"]/div[20]')
        qualificationsinfo = qualificationsdata.xpath('string(.)').extract()
        print qualificationsinfo
        item["qualifications"] = StrUtil.delWhiteSpace(StrUtil.delWhiteSpace(qualificationsinfo[0]))

        return item

    def depose(self):
        self.driver.close()

if __name__ == "__main__":
    uNESCOJobSpider = UNESCOJobSpider()
    uNESCOJobSpider.start()
    uNESCOJobSpider.depose()
