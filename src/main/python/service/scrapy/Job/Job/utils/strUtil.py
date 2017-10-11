# -*- coding: utf-8 -*-
__author__ = 'liuyang'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re

#TODO 字符串工具
class StrUtil(object):

	def __init__(self):
		pass

	@staticmethod
	def delWhiteSpace(msg):
		'''
		将字符串中的空白符换为空格
		'''
		pattern = re.compile('\\s+')
		return (re.sub(pattern, ' ', msg)).strip()

	@staticmethod
	def delMoreSpace(msg):
		'''
		将字符串的多个连续空格转换成一个
		'''
		return ' '.join(msg.split())

	@staticmethod
	def delWhite(msg):
		'''
        删除字符串中的空白符
        '''
		pattern = re.compile('\\s+')
		return (re.sub(pattern, '', msg)).strip()

	@staticmethod
	def isEmpty(msg):
		'''
		判断字符串是否为空
		'''
		return msg and msg.strip()

	@staticmethod
	def completeURL(prefix, url):
		'''
		判断URL是否包含prefix并补全
		'''
		index = prefix.rfind('/')
		url = prefix[0:index + 1] + url
		return url