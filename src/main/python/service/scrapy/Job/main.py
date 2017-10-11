# -*- coding: utf-8 -*-

__author__ = 'liuyang'

'''
scrapy爬虫启动文件，负责全部scrapy爬虫的执行
'''

from scrapy import cmdline

class StartScrapySpider(object):

    def __init__(self):
        pass

    def start(self,name):

        '''
        接收爬虫名，依次执行各爬虫
        :param name: 可以是字符串或者列表 
        '''

        if isinstance(name,str):
            cmdline.execute(("scrapy crawl " + name).split())
        else:
            print "ScrapyError：爬虫执行失败"


if __name__ == "__main__":
    startScrapySpider = StartScrapySpider()
    '''
    爬虫名          任务
    UNDPjob         爬取UNDP岗位
    
    UNDPleaders     爬取UNDP领导人
    
    OECDleaders     爬取OECD领导人

    WIPOleaders     爬取WIPO领导人 

    ESCIjobs        爬取escience岗位
    
    CERNjobs        爬取CERN岗位

    WMOjobs         爬取WMO岗位

    UNIDOjob        爬取UNIDO岗位
    
    UNIDOleader     爬取UNIDO领导人

    UNUjob          爬取UNU岗位
    
    UNUleaders      爬取UNU领导人

    APECleaders     爬取APEC领导人

    IGCEBjobs       爬取IGCEB岗位

    EIAjobs         爬取EIA岗位

    GIFleaders      爬取GIF领导人
    
    WHOjob          爬取WHO岗位
    
    ITERjob         爬取ITER岗位
    '''
    # startScrapySpider.start('UNDPjob')

    # startScrapySpider.start('WHOjob')

    startScrapySpider.start('ITERjob')
    
    # startScrapySpider.start("ESCIjobs")

    # startScrapySpider.start("CERNjobs")

    # startScrapySpider.start('UNIDOjob')
    # startScrapySpider.start('UNIDOleader')

    # startScrapySpider.start('UNUjob -o UNUjob.csv')
    # startScrapySpider.start('UNUleaders -o UNUleaders.csv')

    # startScrapySpider.start('APECleaders -o APECleaders.csv')
    
    # startScrapySpider.start('IGCEBjobs')

    # startScrapySpider.start('EIAjobs -o EIAjobs.csv')

    # startScrapySpider.start('GIFleaders -o GIFleaders.csv')