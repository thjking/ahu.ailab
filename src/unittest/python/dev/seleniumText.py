# -*- coding: utf-8 -*-
from selenium import webdriver

driver = webdriver.PhantomJS(executable_path='phantomjs.exe')
driver.get("https://www.baidu.com/")
print driver.page_source