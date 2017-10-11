# -*- coding: utf-8 -*-
__author__ = 'liuyang'

from twisted.enterprise import adbapi
from mysqlDB import myaqlSave
from ..allitems.jobitems import UNDPJobDataItem,UNDPJobDataItem2,CERNjobDataItem,ICGEBjobDataItem,WHOjobDataItem

class JobPipeline(object):
    # TODO 初始化Mysql
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        name = settings['DB_SERVER']
        dbargs = settings['DB_CONNECT']
        dbpool = adbapi.ConnectionPool(name, **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        if isinstance(item,UNDPJobDataItem):
            self.dbpool.runInteraction(myaqlSave().insertUNDPjob, item)
        elif isinstance(item,UNDPJobDataItem2):
            self.dbpool.runInteraction(myaqlSave().insertUNDP2job, item)
        elif isinstance(item,CERNjobDataItem):
            self.dbpool.runInteraction(myaqlSave().insertCERNjob, item)
        elif isinstance(item,ICGEBjobDataItem):
            self.dbpool.runInteraction(myaqlSave().insertICGEBjob,item)
        elif isinstance(item,WHOjobDataItem):
            self.dbpool.runInteraction(myaqlSave().insertWHOjob, item)
