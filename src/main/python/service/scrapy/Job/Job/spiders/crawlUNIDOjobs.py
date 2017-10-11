# -*- coding: utf-8 -*-
__author__ = 'chenjialin'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import logging.config
from scrapy.http import Request
from ..allitems.jobitems import UNIDOjobDataItem, UNIDOjobDataItem2
from src.main.python.service.scrapy.Job.Job.utils.strUtil import StrUtil
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil
logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger("ahu")

class UNIDOjobLink(scrapy.Spider):
    name = "UNIDOjob"
    start_urls = ["http://www.unido.org/employment/consultancy-opportunities.html",
                  "http://www.unido.org/employment/o518900.html",
                  "http://www.unido.org/overview/employment/internship.html",
                  "http://www.unido.org/internship/internships-in-field-offices.html"]

    def __init__(self):
        self.preurl = 'http://www.unido.org'

    def parse(self, response):
        cnt = 0
        selector = scrapy.Selector(response)
        joburls = selector.xpath('//li[@class="active current activeandsub"]/ul/li/a')

        if response.url == 'http://www.unido.org/internship/internships-in-field-offices.html':
            others = selector.xpath('//div[@class="csc-textpic-text"]/div/table/tbody/tr/td/a')
            for other in others[1:]:
                finalurl = other.xpath('@href').extract()[0]
                if finalurl.endswith('.pdf'):
                    url = self.preurl + finalurl
                    yield Request(url, callback=self.duepdf, dont_filter=True)
                else:
                    pass
        else:
            try:
                for joburl in joburls:
                    url = self.preurl + joburl.xpath('@href').extract()[0]
                    cnt += 1
                    logger.debug('正在抓取<---  ' + url)
                    yield Request(url=url, callback=self.wr)
            except:
                pass
            logger.debug("%s" % response.url + '->>共有'+ str(cnt) + '个招聘信息')

    def wr(self,response):
        selector = scrapy.Selector(response)
        deeps = selector.xpath('//li[@class="active current activeandsub"]/ul/li/a')
        if deeps:
            for deep in deeps:
                url = self.preurl + deep.xpath('@href').extract()[0]
                yield Request(url, callback=self.wr)
            return

        if response.url == 'http://www.unido.org/internship/internships-in-field-offices.html':
            return

        item = self._inititem()
        url = response.url
        item['joburl'] = url
        num = 0

        main_content = selector.xpath('//div[@class="csc-default"]/p')
        itemname = ''
        text = ''
        tips = ''
        totle = 0
        for i in main_content:
            totle += 1

        while num < totle:
            target = ''
            content = main_content[num]
            try:
                target = content.xpath('b/text()').extract()[0]
                text = content.xpath('text()').extract()[0]
            except:
                pass
            num += 1
            if target == 'Duration:' or target == 'Duration: ':
                itemname = 'Duration'
            elif target == 'Duty Station:' or target == 'Duty Station: ':
                itemname = 'Duty_Station'
            elif target == 'Organizational Context:' or target == 'Organizational Context: ':
                itemname = 'Organizational_Context'
            elif target == 'Tasks:' or target == 'Tasks: ':
                itemname = 'Tasks'
                num2 = num
                for content in main_content[num2:]:
                    target = content.xpath('b/text()')
                    if not target:
                        num += 1
                        text += content.xpath('text()').extract()[0]
                    else:
                        break
            elif target == 'Qualification requirements:' or target == 'Qualification requirements: ':
                itemname = 'Requirements'
                num2 = num
                text = ''
                for content in main_content[num2:]:
                    test = content.xpath('text()').extract()[0]
                    if test != u' ':
                        num += 1
                        text += test
                    else:
                        num += 1
                        break
            else:
                try:
                    cont = content.xpath('b')
                    tips += cont.xpath('string(.)').extract()[0]
                except:
                    pass
                continue

            item[itemname] = StrUtil.delWhiteSpace(text)
            logger.debug("UNIDO-->job-->%s" % url+'-->'+itemname+'-->'+item[itemname])

        Work = selector.xpath('//div[@id="header-content"]/div/h1/text()').extract()[0]
        item['Work'] = StrUtil.delWhiteSpace(Work)
        logger.debug("UNIDO-->job-->%s" % url+'-->Work-->'+item['Work'])

        itemname= 'Tips'
        item[itemname] = StrUtil.delWhiteSpace(tips)
        logger.debug("UNIDO-->job-->%s" % url + '-->' + itemname + '-->' + item[itemname])

        itemname = 'link'
        try:
            text = main_content.xpath('a/@href').extract()[0]
            if text:
                item[itemname] = StrUtil.delWhiteSpace(text)
                logger.debug("UNIDO-->job-->%s" % url+'-->'+itemname+'-->'+item[itemname])
        except:
            pass

        yield item

    def duepdf(self, response):
        url = response.url
        items = self._inititem2()
        if url.endswith('.pdf'):
            PDF_name = url.split('/')[-1]
            items['PDF_name'] = StrUtil.delWhiteSpace(PDF_name)
            logger.debug("UNIDO-->job-->%s" % items['PDF_name'])
            yield Request(url, meta={'items': items}, callback=self.savepdf, dont_filter=True)
        else:
            items['Apply_url'] = StrUtil.delWhiteSpace(url)
        yield items

    def savepdf(self, response):
        items = response.meta['items']
        with open('./UNIDOjobs/' + items['PDF_name'], 'wb') as f:
            f.write(response.body)

    def _inititem(self):
        '''
        初始化全部字段
        :return: 初始字段
        '''
        item = UNIDOjobDataItem()
        item['englishname'] = 'UNIDO'  # 组织英文缩写
        item['chinesename'] = '联合国工业发展组'  # 组织中文缩写
        item['incontinent'] = '欧洲'  # 组织所属洲
        item['incountry'] = '奥地利'  # 组织所在国家
        item['type'] = '经济'  # 组织类别
        item['url'] = 'www.unido.org'  # 组织主页
        item['Work'] = ''         #岗位名称
        item['Duration'] = ''     #工作时长
        item['Duty_Station'] = '' #工作地点
        item['Organizational_Context'] = '' #组织背景
        item['Tasks'] = ''        #岗位描述
        item['Requirements'] = '' #资格要求
        item['Tips'] = ''         #相关信息
        item['joburl'] = ''       #招聘页面
        item['link'] = ''         #申请链接
        return item

    def _inititem2(self):
        items = UNIDOjobDataItem2()
        items['englishname'] = 'UNIDO'  # 组织英文缩写
        items['chinesename'] = '联合国工业发展组'  # 组织中文缩写
        items['incontinent'] = '欧洲'  # 组织所属洲
        items['incountry'] = '奥地利'  # 组织所在国家
        items['type'] = '经济'  # 组织类别
        items['url'] = 'www.unido.org'  # 组织主页
        return items


