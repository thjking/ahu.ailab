import logging.config
import sys
import urllib

import scrapy
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil

# -*- coding: utf-8 -*-
__author__ = 'DelusionLW'

reload(sys)


logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')


class GIFleadersSpider(scrapy.Spider):
    name = "EIAjobs"

    allowed_domains = ["https://www.eia.gov/"]

    start_urls = ["https://www.eia.gov/about/careers/index.php"]

    def __init__(self):
        logger.debug("Start parse every jobs information")
        self.url = "https://www.eia.gov/"

    def parse(self, response):

        selector = scrapy.Selector(response)

        if response.url.endswith('index.php'):   # todo Parse jobs
            logger.info("Open jobs' information successfully. Start parse:")
            cvs = selector.xpath('//div[@class="main_col"]//li/a')

            for cv in cvs:
                try:
                    ur = cv.xpath('@href').extract()[0]
                    url = "https://www.eia.gov/about/careers/" + ur
                    urllib.urlretrieve(url, ur)
                    # logger.debug("Start parse job pdf")
                    # yield Request(url=ur, callback=_parseEIAjobs)
                except:
                    pass

