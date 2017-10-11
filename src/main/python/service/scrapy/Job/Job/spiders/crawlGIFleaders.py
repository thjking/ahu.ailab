import logging.config
import re
import sys

import scrapy
from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil

from ..allitems.leaderitems import GIFLeadersItem

# -*- coding: utf-8 -*-
__author__ = 'DelusionLW'

reload(sys)


logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')


class GIFleadersSpider(scrapy.Spider):
    name = "GIFleaders"

    allowed_domains = ["https://www.gen-4.org/gif/jcms/c_9260/public"]

    start_urls = ["https://www.gen-4.org/gif/jcms/c_9528/who-s-who"]

    def __init__(self):
        logger.debug("Start parse every member's information")
        self.url = "https://www.gen-4.org/gif/jcms/c_9260/public"

    def parse(self, response):

        selector = scrapy.Selector(response)

        if response.url.endswith('c_9528/who-s-who'):   # todo Parse member's information
            logger.info("Open member's information successfully. Start parse:")
            item = self._inititem()
            cvs = selector.xpath('//table[@class="table table-condensed"]//td').extract()

            i = 1
            while i <= len(cvs):
                if i % 2 != 0:
                    first = re.search('<strong>', cvs[i]).span()[1]
                    end = re.search('</strong>', cvs[i]).span()[0]
                    item["name"] = cvs[i][first:end]
                    item["url"] = response.url
                    first = re.search('</strong>', cvs[i]).span()[1]
                    end = cvs[i].rfind('.', first, len(cvs[i]))
                    item["info"] = cvs[i][first:end]

                    yield item

                i += 1

    def _inititem(self):

        '''

        :return:
        '''
        item = GIFLeadersItem()
        item["name"] = ''
        item["info"] = ''
        logger.info('Initialize members information ')
        return item
