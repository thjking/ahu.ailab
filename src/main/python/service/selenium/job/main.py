# -*- coding: utf-8 -*-

__author__ = 'Robin'


import os

def run(name):
    if isinstance(name, str):
        os.system(("python " + name + ".py"))
    else:
        print "SeleniumError：爬虫执行失败"

def main():

    run('crawlITERjobs')

    # run('crawlOECDjobs')

    # run('crawlWHOjobs')
    
    # run('crawlWIPOjobs')

    # run('crawUNESCOjobs')

if __name__ == "__main__":
    main()
    