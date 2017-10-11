# -*- coding: utf-8 -*-
#writen by Jing
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
from ..allitems.leaderitems import APECLeadersItem
from src.main.python.service.scrapy.Job.Job.utils.strUtil import StrUtil
import logging.config
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

class APECleadersSpider(scrapy.Spider):
    name = "APECleaders"

    allowed_domins = ["http://www.apec.org/"]

    start_urls = ["https://www.apec.org/ContactUs/APECSecretatriat"]

    def __init__(self):
        logger.debug("开始爬取APEC领导人信息")
        self.url = "http://www.apec.org/"

    def parse(self, response):
        item = self._inititem()
        item["url"] = response.url
        selector = scrapy.Selector(response)
        links1 = selector.xpath('//table[@class="contact-list"][2]/tbody/tr')
#        print links
        if links1:
            for i in range(0,len(links1)):
#                print i
#                print len(links)
#                print links[i].extract()
                Firstname = links1[i].xpath('td[1]//strong/text()').extract()    #相同的标签套标签直接用//
                Givenname = links1[i].xpath('td[1]/strong/text()').extract()
                name = Firstname[0] + Givenname[0]          #名字分两段表示
#                print name

                email = links1[i].xpath('td[1]/a/@href').extract()
#                print email
                work = links1[i].xpath('td[2]/text()').extract()
#                print work[0]
                assistant = links1[i].xpath('td[3]')
                assistantName = assistant.xpath('string(.)').extract()      #由于存在空标签 所以采用取字符串
#                print assistantName[0]


                if name:
                    item['name'] = StrUtil.delWhiteSpace(name)

                if email:
                    item['email'] = StrUtil.delWhiteSpace(email[0][7:]) #第7字符个开始为email

                if work:
                    item['work'] = StrUtil.delWhiteSpace(work[0])


                if assistantName:
                    item['assistant'] = StrUtil.delWhiteSpace(assistantName[0])


                logger.debug('>>>APECleader>>>name>>>%s' % item["name"])
                logger.debug('>>>APECleader>>>email>>>%s' % item["email"])
                logger.debug('>>>APECleader>>>work>>>%s' % item["work"])
                logger.debug('>>>APECleader>>>assistant>>>%s' % item["assistant"])

                yield item
        else:
            logger.error('爬取APEC领导人1失败')

        ###############################
        links3 = selector.xpath('//table[@class="contact-list"][3]/tr')
        if links3:
            for i in range(0, len(links3)):

                name = links3[i].xpath('td[1]/h2/text()').extract()

                email = links3[i].xpath('td[1]/p/a/@href').extract()
#                print email
                work = links3[i].xpath('td[2]/text()').extract()
#                print work[0]
                assistant = links3[i].xpath('td[3]')
                assistantName = assistant.xpath('string(.)').extract()  # 由于存在空标签 所以采用取字符串
#                print assistantName[0]

                if name:
                    item['name'] = StrUtil.delWhiteSpace(name[0])

                if email:
                    item['email'] = StrUtil.delWhiteSpace(email[0][7:])  # 第7字符个开始为email

                if work:
                    item['work'] = StrUtil.delWhiteSpace(work[0])

                if assistantName:
                    item['assistant'] = StrUtil.delWhiteSpace(assistantName[0])

                logger.debug('>>>APECleader>>>name>>>%s' % item["name"])
                logger.debug('>>>APECleader>>>email>>>%s' % item["email"])
                logger.debug('>>>APECleader>>>work>>>%s' % item["work"])
                logger.debug('>>>APECleader>>>assistant>>>%s' % item["assistant"])

                yield item
        else:
            logger.error('爬取APEC领导人3失败')

        links4 = selector.xpath('//table[@class="contact-list"][4]/tbody/tr')
        #        print links
        if links4:
            for i in range(0, len(links4)):

                Firstname = links4[i].xpath('td[1]//strong/text()').extract()  # 相同的标签套标签直接用//
                Givenname = links4[i].xpath('td[1]/strong/text()').extract()
                name = Firstname[0] + Givenname[0]  # 名字分两段表示
#                print name

                email = links4[i].xpath('td[1]/a/@href').extract()
#                print email
                work = links4[i].xpath('td[2]/text()').extract()
#                print work[0]
                assistant = links4[i].xpath('td[3]')
                assistantName = assistant.xpath('string(.)').extract()  # 由于存在空标签 所以采用取字符串
#                print assistantName[0]

                if name:
                    item['name'] = StrUtil.delWhiteSpace(name)

                if email:
                    item['email'] = StrUtil.delWhiteSpace(email[0][7:])  # 第7字符个开始为email

                if work:
                    item['work'] = StrUtil.delWhiteSpace(work[0])

                if assistantName:
                    item['assistant'] = StrUtil.delWhiteSpace(assistantName[0])

                logger.debug('>>>APECleader>>>name>>>%s' % item["name"])
                logger.debug('>>>APECleader>>>email>>>%s' % item["email"])
                logger.debug('>>>APECleader>>>work>>>%s' % item["work"])
                logger.debug('>>>APECleader>>>assistant>>>%s' % item["assistant"])

                yield item
        else:
            logger.error('爬取APEC领导人4失败')

        ###########################################
        links5 = selector.xpath('//table[@class="contact-list"][5]/tbody/tr')
        #        print links
        if links5:
            for i in range(0, len(links5)):
                name = links5[i].xpath('td[1]//strong/text()').extract()  # 相同的标签套标签直接用//


                email = links5[i].xpath('td[1]/a/@href').extract()
#                print email
                work = links5[i].xpath('td[2]/text()').extract()
#                print work[0]
                assistant = links5[i].xpath('td[3]')
                assistantName = assistant.xpath('string(.)').extract()  # 由于存在空标签 所以采用取字符串
#                print assistantName[0]

                if name:
                    item['name'] = StrUtil.delWhiteSpace(name[-1])      #某处font格式设计使人费解，难以爬取，从后面选

                if email:
                    item['email'] = StrUtil.delWhiteSpace(email[0][7:])  # 第7字符个开始为email

                if work:
                    item['work'] = StrUtil.delWhiteSpace(work[0])

                if assistantName:
                    item['assistant'] = StrUtil.delWhiteSpace(assistantName[0])

                logger.debug('>>>APECleader>>>name>>>%s' % item["name"])
                logger.debug('>>>APECleader>>>email>>>%s' % item["email"])
                logger.debug('>>>APECleader>>>work>>>%s' % item["work"])
                logger.debug('>>>APECleader>>>assistant>>>%s' % item["assistant"])

                yield item
        else:
            logger.error('爬取APEC领导人5失败')
        ###############################################
        links6 = selector.xpath('//table[@class="contact-list"][6]/tbody/tr')
        #        print links
        if links6:
            for i in range(0, len(links6)):
                Firstname = links6[i].xpath('td[1]//strong/text()').extract()  # 相同的标签套标签直接用//
                Givenname = links6[i].xpath('td[1]/strong/text()').extract()
                name = Firstname[0] + Givenname[0]  # 名字分两段表示
#                print name

                email = links6[i].xpath('td[1]/a/@href').extract()
#                print email
                work = links6[i].xpath('td[2]/text()').extract()
#                print work[0]
                assistant = links6[i].xpath('td[3]')
                assistantName = assistant.xpath('string(.)').extract()  # 由于存在空标签 所以采用取字符串
#                print assistantName[0]

                if name:
                    item['name'] = StrUtil.delWhiteSpace(name)

                if email:
                    item['email'] = StrUtil.delWhiteSpace(email[0][7:])  # 第7字符个开始为email

                if work:
                    item['work'] = StrUtil.delWhiteSpace(work[0])

                if assistantName:
                    item['assistant'] = StrUtil.delWhiteSpace(assistantName[0])

                logger.debug('>>>APECleader>>>name>>>%s' % item["name"])
                logger.debug('>>>APECleader>>>email>>>%s' % item["email"])
                logger.debug('>>>APECleader>>>work>>>%s' % item["work"])
                logger.debug('>>>APECleader>>>assistant>>>%s' % item["assistant"])

                yield item
        else:
            logger.error('爬取APEC领导人6失败')

        ############################################


    def _inititem(self):
        '''
        初始化全部字段
        :return:
        '''
        item = APECLeadersItem()
        item["name"] = ""
        item["work"] = ""
        item["email"] = ""
        item["assistant"] = ""
        logger.info('初始化APEC领导人和item成功')
        return item
