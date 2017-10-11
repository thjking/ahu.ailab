# -*- coding:utf-8 -*-
__author__ = 'liuyang'
from selenium import webdriver
from scrapy.http import HtmlResponse
from lxml import etree
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.resourceTimeout"] = 30

driver = webdriver.PhantomJS()
# driver = webdriver.Chrome()
driver.maximize_window()

class SeleniumMiddleware(object):
    '''
    selenium中间件，对于js加载的页面，Request请求经过该中间件经phantomjs渲染后返回
    '''

    def process_request(self, request, spider):
        if spider.name == 'UNDPjob' and request.url.endswith('id=2'):
            try:
                driver.get(request.url)
                driver.implicitly_wait(10)
                origin_page = driver.page_source
                soup = BeautifulSoup(origin_page, 'html.parser')
                # origin_html = etree.HTML(origin_page)
                link = soup.find('iframe').get('src')
                driver.get(link)
                driver.implicitly_wait(10)
                true_page = driver.page_source
                return HtmlResponse(request.url, body=true_page, encoding='utf-8', request=request, )
            except:
                print "get UNDPjob data failed"
                raise Exception()

        elif spider.name == 'WHOjob':
            try:
                driver.get(request.url)
                driver.implicitly_wait(5)
                time.sleep(1)
                true_page = driver.page_source  # .decode('utf-8','ignore')
                return HtmlResponse(request.url, body=true_page, encoding='utf-8', request=request, )
            except:
                print "get WHOjob data failed"
                raise Exception()
        else:
            pass

def close_driver():
    driver.close()