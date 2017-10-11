# -*- coding:utf-8 -*-
__author__ = 'LiuYang'

import sys, os
import pickle
import shutil

class FileUtil(object):

    '''
    文件处理类
    '''

    def __init__(self):
        pass

    def writeObjToFile(self,fileName,obj):
        """
        将python对象写入文件
        """
        with open(fileName, 'wb') as f:
            pickle.dump(obj, f)

    def readFileToObj(self,fileName):
        """
        从文件读取python对象
        """
        if os.path.exists(fileName):
            with open(fileName, 'rb') as f:
                obj = pickle.load(f)
                return obj

    def deleteFile(self,fileName):
        """
        删除文件
        """
        if os.path.exists(fileName):
            os.remove(fileName)
            return True
        else:
            return False

    def cur_file_dir(self):
        """
       获取脚本文件的当前路径
       """
        # 获取脚本路径
        path = sys.path[0]
        # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path)

    def getLogConfigPath(self, rootFolder="ahu.ailab"):
        """
        获取logging配置文件的路径
        """
        logPath = self.cur_file_dir().split(rootFolder, 1)[0] + rootFolder + "/src/main/scripts/logging.ini"
        # print logPath
        return logPath

    def getResoursePath(self,rootFolder="ahu.ailab"):
        """
        获取资源文件路径
        """
        resoursePath = self.cur_file_dir().split(rootFolder,1)[0] + rootFolder + "/src/main/python/resourse"
        # print resoursePath
        return resoursePath

    def move(self,source_path,target_path):
        """
        移动文件到指定文件夹下
        """
        if os.path.exists(source_path):
            shutil.move(source_path,target_path)
            return True
        else:
            return False