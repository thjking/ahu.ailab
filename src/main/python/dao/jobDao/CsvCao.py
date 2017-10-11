# -*- coding: utf-8 -*-
__author__ = 'Liuyang'

import csv
import logging.config

from src.main.python.service.scrapy.Job.Job.utils.FileUtil import FileUtil

logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger("ahu")

class SaveToCsv(object):

    def __init__(self):
        self.path = FileUtil().getResoursePath() + "/data/jobData/"

    def saveWHOjobs(self,org,items):
        '''
        保存爬取的WHO数据到csv文件
        :return: 
        '''
        csvfile = file(self.path + org, 'wb')
        writer = csv.writer(csvfile)
        title = ("englishname","chinesename","incontinent","incountry","type","url","alljoburl","joburl","work","Location","PostLevel",\
                 "ContractualArrangement","ClosingDate","Contractduration","PrimaryLocation","JobPosting","Organization","Schedule")
        writer.writerow(title)
        # TODO 遍历每条数据,写入csv
        for item in items:
            data = (item["englishname"],item["chinesename"],item["incontinent"],item["incountry"],item["type"], \
                    item["url"],item["alljoburl"],item["joburl"],item["work"],item["Location"],item["PostLevel"], \
                    item["ContractualArrangement"],item["ClosingDate"],item["Contractduration"], \
                    item["PrimaryLocation"],item["JobPosting"],item["Organization"],item["Schedule"])
            try:
                writer.writerow(data)
            except Exception,e:
                print e
        csvfile.close()

    def saveOECDjobs(self,org,items):
        '''
        保存爬取的OECD数据到csv文件
        :return: 
        '''
        csvfile = file(self.path + org, 'wb')
        writer = csv.writer(csvfile)
        title = ("englishname","chinesename","incontinent","incountry","type","url","alljoburl","work","Description","MainResponsibilities",\
                 "IdealCandidateProfile","Contract","offers")
        writer.writerow(title)
        # TODO 遍历每条数据,写入csv
        for item in items:
            data = (item["englishname"],item["chinesename"],item["incontinent"],item["incountry"],item["type"], \
                    item["url"],item["alljoburl"],item["work"].encode('utf-8'),item["Description"].encode('utf-8'), \
                    item["MainResponsibilities"].encode('utf-8'), item["IdealCandidateProfile"].encode('utf-8'), \
                    item["Contract"].encode('utf-8'), item["offers"].encode('utf-8'))
            try:
                writer.writerow(data)
            except Exception,e:
                print e
        csvfile.close()

    def saveWIPOjobs(self,org,items):
        '''
        保存爬取的WIPO数据到csv文件
        :return: 
        '''
        csvfile = file(self.path + org, 'wb')
        writer = csv.writer(csvfile)
        title = ("englishname","chinesename","incontinent","incountry","type","url","alljoburl","joburl","work","sector","grade",\
                 "ContractDuration","DutyStation","PublicationDate","ApplicationDeadline","Organizationalcontext","Dutiesandresponsibilities",\
                 "Requirements","Organizationalcompetencies","Information")
        writer.writerow(title)
        # TODO 遍历每条数据,写入csv
        for item in items:
            data = (item["englishname"],item["chinesename"],item["incontinent"],item["incountry"],item["type"], \
                    item["url"],item["alljoburl"],item["joburl"],item["work"].encode('utf-8'),item["sector"].encode('utf-8'),item["grade"].encode('utf-8'), \
                    item["ContractDuration"].encode('utf-8'),item["DutyStation"].encode('utf-8'),item["PublicationDate"].encode('utf-8'), \
                    item["ApplicationDeadline"].encode('utf-8'),item["Organizationalcontext"].encode('utf-8'),item["Dutiesandresponsibilities"].encode('utf-8'),\
                    item["Requirements"].encode('utf-8'),item["Organizationalcompetencies"].encode('utf-8'),item["Information"].encode('utf-8'))
            try:
                writer.writerow(data)
            except Exception,e:
                print e
        csvfile.close()

    def saveITERjobs(self,org,items):
        '''
        保存爬取的ITER数据到csv文件
        :return: 
        '''
        csvfile = file(self.path + org, 'wb')
        writer = csv.writer(csvfile)
        title = ('Jobtitle' ,'Main job', 'joburl', 'Department', 'Division', 'Job Family', "Application Deadline (MM/DD/YYYY)", 'Grade', 'Direct employment', 'Purpose', "Main duties / Responsibilities", 'Measures of effectiveness', 'Level of study', 'Diploma', 'Level of experience', "Technical experience/knowledge", 'Social skills', 'Specific skills', 'General skills', 'Others', 'Languages')
        writer.writerow(title)
        # TODO 遍历每条数据,写入csv
        # for item in items:
        #     data = (item['Jobtitle'].encode('utf-8'), item["Main job"].encode('utf-8'), item["Department"].encode('utf-8'), item["Division"].encode('utf-8'), item["Job Family"].encode('utf-8'), item["Application Deadline (MM/DD/YYYY)"].encode('utf-8'), item["Grade"].encode('utf-8'), item["Direct employment"].encode('utf-8'), item["Purpose"].encode('utf-8'), item["Main duties / Responsibilities"].encode('utf-8'), item["Measures of effectiveness"].encode('utf-8'), item["Level of study"].encode('utf-8'), item["Diploma"].encode('utf-8'), item["Technical experience/knowledge"].encode('utf-8'), item["Social skills"].encode('utf-8'), item["Specific skills"].encode('utf-8'), item["General skills"].encode('utf-8'), item["Others"].encode('utf-8'), item["Languages"].encode('utf-8'))
        for item in items:
            data = []
            for i in title:
                # print i
                try:
                    data.append(item[i].encode('utf-8'))
                except:
                    print item['Jobtitle'] + " hasn't key: " + i
            try:
                writer.writerow(tuple(data))
            except Exception,e:
                print e
        csvfile.close()

    def saveESCIjobs(self,org,items):
        '''
        保存爬取的ESCI数据到csv文件
        :return: 
        '''
        csvfile = file(self.path + org, 'wb')
        writer = csv.writer(csvfile)
        title = ['jobname', 'companyname', 'position', 'date', 'Job description', 'Job reference', 'Publication date', 'closing date', 'Introduction', 'Functions', 'Qualification required', 'Experience and competencies', 'Eligibility conditions', 'Note on Employment Conditions', 'Jobtitle' , 'Main job', 'Department', 'Division', 'Job Family', "Application Deadline (MM/DD/YYYY)", 'Grade', 'Direct employment', 'Purpose', "Main duties / Responsibilities", 'Measures of effectiveness', 'Level of study', 'Diploma', 'Level of experience', "Technical experience/knowledge", 'Social skills', 'Specific skills', 'General skills', 'Others', 'Languages', 'POSITION', 'REFERENCE NO.', 'LOCATION', 'Timezone', 'CLOSING DATE', 'United Nations University objectives', 'UNU Vice-Rectorate in Europe (UNU-ViE)', 'UNU Computing and Society (UNU-CS)', 'UNU Institute for Environment and Human Security (UNU-EHS)', 'Responsibilities', 'Main duties and responsibilities', 'Required qualifications and competencies', 'Remuneration', 'Duration of contract', 'Starting date', 'context', 'Job summary']
        writer.writerow(tuple(title))
        # TODO 遍历每条数据,写入csv
        # print len(items)
        for item in items:
            data = []
            # print title
            for i in title:
                try:
                    data.append(item[i].encode('utf-8'))
                except:
                    data.append(' ')
            # data = (item['jobname'], item['companyname']
            #     item['Jobtitle'].encode('utf-8'), item["Main job"].encode('utf-8'), item["Department"].encode('utf-8'), item["Division"].encode('utf-8'), item["Job Family"].encode('utf-8'), item["Application Deadline (MM/DD/YYYY)"].encode('utf-8'), item["Grade"].encode('utf-8'), item["Direct employment"].encode('utf-8'), item["Purpose"].encode('utf-8'), item["Main duties / Responsibilities"].encode('utf-8'), item["Measures of effectiveness"].encode('utf-8'), item["Level of study"].encode('utf-8'), item["Diploma"].encode('utf-8'), item["Technical experience/knowledge"].encode('utf-8'), item["Social skills"].encode('utf-8'), item["Specific skills"].encode('utf-8'), item["General skills"].encode('utf-8'), item["Others"].encode('utf-8'), item["Languages"].encode('utf-8'), \

            # )
            try:
                writer.writerow(tuple(data))
            except Exception,e:
                print e
        csvfile.close()

    def saveCERNjobs(self,org,items):
        '''
        保存爬取的CERN数据到csv文件
        :return: 
        '''
        csvfile = file(self.path + org, 'wb')
        writer = csv.writer(csvfile)
        title = ['Job title', 'joburl', 'Job description', 'Job reference', 'Publication date', 'closing date', 'Introduction', 'Functions', 'Qualification required', 'Experience and competencies', 'Eligibility conditions', 'Note on Employment Conditions']
        writer.writerow(tuple(title))
        # TODO 遍历每条数据,写入csv
        # print len(items)
        for item in items:
            data = []
            # print title
            for i in title:
                try:
                    data.append(item[i].encode('utf-8'))
                except:
                    data.append(' ')
            
            try:
                writer.writerow(tuple(data))
            except Exception,e:
                print e
        csvfile.close()

    def saveUNDP2jobs(self, org, items):
        '''
        保存爬取的CERN数据到csv文件
        :return: 
        '''
        csvfile = file(self.path + org, 'wb')
        writer = csv.writer(csvfile)
        title = ['Agency', 'Title', 'joburl', 'JobID', 'PracticeAreaJobFamily', 'VacancyEndDate', 'TimeLeft', 'DutyStation', 'EducationWorkExperience', 'Languages', 'Grade', 'VacancyType', 'PostingType', 'Bureau', 'ContractDuration', 'Background', 'DutiesandResponsibilities', 'Competencies', 'RequiredSkillsandExperience', 'Disclaimer']
        writer.writerow(tuple(title))
        # TODO 遍历每条数据,写入csv
        # print len(items)
        for item in items:
            data = []
            # print title
            for i in title:
                try:
                    data.append(item[i].encode('utf-8'))
                except:
                    data.append(' ')
            
            try:
                writer.writerow(tuple(data))
            except Exception,e:
                print e
        csvfile.close()