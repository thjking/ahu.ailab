# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class UNDPJobDataItem(scrapy.Item):
    englishname = scrapy.Field() #组织英文缩写
    chinesename = scrapy.Field() #组织中文名称
    incontinent = scrapy.Field() #组织所属洲
    incountry = scrapy.Field()   #组织所在国家
    type = scrapy.Field()        #组织类别
    url = scrapy.Field()         #组织主页
    alljoburl = scrapy.Field()   #组织招聘岗位主页
    joburl = scrapy.Field()      #该招聘岗位主页
    describe = scrapy.Field()    #岗位描述
    suoshu = scrapy.Field()      #所属机构
    work = scrapy.Field()        #岗位名称
    applytime = scrapy.Field()   #申请截止时间
    linkman = scrapy.Field()     #岗位联系人
    Location = scrapy.Field()    #位置
    ApplicationDeadline = scrapy.Field() #申请截至时间
    TypeofContract = scrapy.Field() #包工方式
    PostLevel = scrapy.Field()   #职位级别
    LanguagesRequired = scrapy.Field()   #语言要求
    DurationofInitialContract = scrapy.Field()   #初始合同时间
    ExpectedDurationofAssignment = scrapy.Field()   #预计工作时间
    AdditionalCategory  = scrapy.Field()   #额外的类别
    Background = scrapy.Field()         #背景
    DutiesandResponsibilities = scrapy.Field()           #工作职责
    Competencies = scrapy.Field()       #能力
    RequiredSkillsandExperience = scrapy.Field()        #技能和经历

class UNDPJobDataItem2(scrapy.Item):

    englishname = scrapy.Field() #组织英文缩写
    chinesename = scrapy.Field() #组织中文名称
    incontinent = scrapy.Field() #组织所属洲
    incountry = scrapy.Field()   #组织所在国家
    type = scrapy.Field()        #组织类别
    url = scrapy.Field()         #组织主页
    alljoburl = scrapy.Field()   #组织招聘岗位主页
    joburl = scrapy.Field()      #该招聘岗位主页
    describe = scrapy.Field()    #岗位描述
    suoshu = scrapy.Field()      #所属机构
    applytime = scrapy.Field()   #申请截止时间
    linkman = scrapy.Field()     #岗位联系人
    Agency = scrapy.Field()      #代理
    Title = scrapy.Field()       #岗位名称
    JobID = scrapy.Field()       #岗位id
    PracticeAreaJobFamily = scrapy.Field()     #实习区
    VacancyEndDate = scrapy.Field()   #工作地点
    TimeLeft = scrapy.Field()       #剩余时间
    DutyStation = scrapy.Field()
    EducationWorkExperience = scrapy.Field()   #教育和工作经历
    Languages = scrapy.Field()  # 语言
    Grade = scrapy.Field()   #职级
    VacancyType = scrapy.Field()  # 空缺类型
    PostingType = scrapy.Field()
    Bureau = scrapy.Field()  # 办公室
    ContractDuration = scrapy.Field()  # 合同期
    Background = scrapy.Field()         #背景
    DutiesandResponsibilities = scrapy.Field()        #义务与责任
    Competencies = scrapy.Field()       #能力
    RequiredSkillsandExperience = scrapy.Field()        #技能和经历
    Disclaimer = scrapy.Field()        #免责


# class ITERjobDataItem2(scrapy.Item):
    
#     englishname = scrapy.Field() #组织英文缩写
#     chinesename = scrapy.Field() #组织中文名称
#     incontinent = scrapy.Field() #组织所属洲
#     incountry = scrapy.Field()   #组织所在国家
#     type = scrapy.Field()        #组织类别
#     url = scrapy.Field()         #组织主页
#     alljoburl = scrapy.Field()   #组织招聘岗位主页
#     joburl = scrapy.Field()      #该招聘岗位主页

class ITERjobDataItem(scrapy.Item):
    englishname = scrapy.Field()  # 组织英文缩写
    chinesename = scrapy.Field()  # 组织中文缩写
    incontinent = scrapy.Field()  # 组织所属洲
    incountry = scrapy.Field()  # 组织所在国家
    type = scrapy.Field()  # 组织类别
    url = scrapy.Field()  # 组织主页
    alljoburl = scrapy.Field()  # 组织招聘岗位主页
    joburl = scrapy.Field()  # 该岗位链接
    JobTitle = scrapy.Field()
    Division = scrapy.Field()
    Others = scrapy.Field()
    Diploma = scrapy.Field() #毕业证书

    JobDetailUrl = scrapy.Field()
    MainJob = scrapy.Field()
    Department = scrapy.Field()

    Section = scrapy.Field()
    JobFamily = scrapy.Field()
    ApplicationDeadline = scrapy.Field()
    Grade = scrapy.Field()
    DirectEmployment = scrapy.Field()
    Purpose = scrapy.Field()
    MainDuties = scrapy.Field()
    MeasuresOfEffectiveness = scrapy.Field()
    LevelOfExperience = scrapy.Field()
    Knowledge = scrapy.Field()
    SocialSkills = scrapy.Field()
    SpecificSkills = scrapy.Field()
    GeneralSkills = scrapy.Field()
    Languages = scrapy.Field()



class UNUjobDataItem(scrapy.Item):
    englishname = scrapy.Field()   #组织英文缩写
    chinesename = scrapy.Field()   #组织中文缩写
    incontinent = scrapy.Field()     #组织所属洲
    incountry = scrapy.Field()   #组织所在国家
    type = scrapy.Field()        #组织类别
    url = scrapy.Field()         #组织主页
    alljoburl = scrapy.Field()   #组织招聘岗位主页
    joburl = scrapy.Field()     #该岗位链接
    outurl = scrapy.Field()      #岗位外部链接
    describe = scrapy.Field()    #岗位描述
    Title = scrapy.Field()        #岗位名称
    applytime = scrapy.Field()   #申请截止时间
    recruitment = scrapy.Field()  #招聘组织信息
    starting_date = scrapy.Field() #开始日期
    location = scrapy.Field()      #开设国家
    application_procedure = scrapy.Field()  #申请流程

class UNIDOjobDataItem(scrapy.Item):
    englishname = scrapy.Field()   #组织英文缩写
    chinesename = scrapy.Field()   #组织中文缩写
    incontinent = scrapy.Field()     #组织所属洲
    incountry = scrapy.Field()   #组织所在国家
    type = scrapy.Field()        #组织类别
    url = scrapy.Field()         #组织主页
    Work = scrapy.Field()
    Duration = scrapy.Field()  # 工作时长
    Duty_Station = scrapy.Field()  # 工作地点
    Organizational_Context = scrapy.Field()  # 组织背景
    Tasks = scrapy.Field()  # 岗位描述
    Requirements = scrapy.Field()  # 资格要求
    Tips = scrapy.Field()  # 相关信息
    joburl = scrapy.Field()  # 招聘页面
    link = scrapy.Field()  # 相关知识链接

class UNIDOjobDataItem2(scrapy.Item):
    englishname = scrapy.Field()   #组织英文缩写
    chinesename = scrapy.Field()   #组织中文缩写
    incontinent = scrapy.Field()   #组织所属洲
    incountry = scrapy.Field()   #组织所在国家
    type = scrapy.Field()        #组织类别
    url = scrapy.Field()         #组织主页
    PDF_name = scrapy.Field()     #PDF文件名

class ICGEBjobDataItem(scrapy.Item):
    englishname = scrapy.Field()  # 组织英文缩写
    chinesename = scrapy.Field()  # 组织中文名称
    incontinent = scrapy.Field()  # 组织所属洲
    incountry = scrapy.Field()  # 组织所在国家
    type = scrapy.Field()  # 组织类别
    url = scrapy.Field()  # 组织主页
    alljoburl = scrapy.Field()  # 组织招聘岗位主页
    location = scrapy.Field()   #位置
    require = scrapy.Field()    #要求
    work = scrapy.Field()  #职位
    deadline = scrapy.Field()   #截止日期
    applymethod = scrapy.Field()    #申请方法
    joburl = scrapy.Field()    #该招聘岗位主页

class CERNjobDataItem(scrapy.Item):
    englishname = scrapy.Field()  # 组织英文缩写
    chinesename = scrapy.Field()  # 组织中文名称
    incontinent = scrapy.Field()  # 组织所属洲
    incountry = scrapy.Field()  # 组织所在国家
    type = scrapy.Field()  # 组织类别
    url = scrapy.Field()  # 组织主页
    alljoburl = scrapy.Field()  # 组织招聘岗位主页
    joburl = scrapy.Field()  # 该招聘岗位主页
    Jobtitle = scrapy.Field()
    Jobdescription = scrapy.Field()
    Jobreference = scrapy.Field()
    Publicationdate = scrapy.Field()
    closingdate = scrapy.Field()
    Introduction = scrapy.Field()
    Functions = scrapy.Field()
    QualificationRequired = scrapy.Field()
    ExperienceandCompetencies = scrapy.Field()
    EligibilityConditions = scrapy.Field()
    NoteonEmploymentConditions = scrapy.Field()

class WHOjobDataItem(scrapy.Item):
    englishname = scrapy.Field()  # 组织英文缩写
    chinesename = scrapy.Field()  # 组织中文名称
    incontinent = scrapy.Field()  # 组织所属洲
    incountry = scrapy.Field()  # 组织所在国家
    type = scrapy.Field()  # 组织类别
    url = scrapy.Field()  # 组织主页
    alljoburl = scrapy.Field()  # 组织招聘岗位主页
    joburl = scrapy.Field()  # 该招聘岗位主页
    work = scrapy.Field()  # 岗位
    Location = scrapy.Field()  # 位置
    PostLevel = scrapy.Field()  # 职级
    ContractualArrangement = scrapy.Field()  # 合同安排
    ClosingDate = scrapy.Field()  # 截止日期
    Contractduration = scrapy.Field()  # 合同期限
    PrimaryLocation = scrapy.Field()  # 主要地点
    JobPosting = scrapy.Field()  # 工作公告
    Organization = scrapy.Field()  # 组织
    Schedule = scrapy.Field()  # 是否全职
    Required = scrapy.Field()  # 要求



