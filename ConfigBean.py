#!/bin/python
#coding=gbk
import configparser
import xml.etree.ElementTree as ET

def booltostr(bnum):
    if(bnum == True):
        return "True"
    else:
        return "False"
class Login:

    def __init__(self):
        self.mName = 'login'
        self.mMethod = 'get'
        self.mUrl = None
        self.mNeed = False
        self.mFields = dict()
    def tostring(self):
        return("mName="+self.mName+";mMethod="+self.mMethod+";mUrl=" +self.mUrl+ ";mNeed="+booltostr(self.mNeed) +":mFields="+str(self.mFields) )
class Cookies:
    def __init__(self):
        self.mName='cookies'
        self.mNeed = False
        self.mFields = dict()
    def tostring(self):
        return("mName="+self.mName+";mNeed="+booltostr(self.mNeed)+":mFields="+str(self.mFields))
class Headers:
    def __init__(self):
        self.mName = 'headers'
        self.mNeed = False
        self.mFields = dict()
    def tostring(self):
        return("mName="+self.mName+";mNeed="+booltostr(self.mNeed)+":mFields="+str(self.mFields))

class Filter:
    def __init__(self):
        self.mName = 'filter'
        self.mNeed = False
        self.mFields = dict()
    def tostring(self):
        return("mName="+self.mName+";mNeed="+booltostr(self.mNeed)+":mFields="+str(self.mFields))

class Logic:
    def __init__(self):
        self.mName = 'filter'
        self.mNeed = False
        self.mFields = dict()
    def tostring(self):
        return("mName="+self.mName+";mNeed="+booltostr(self.mNeed)+":mFields="+str(self.mFields))

class ConfigBean:
    def __init__(self,config_xml):
        self.mPostdata = None
        self.mHeader = None
        self.mNeedlogin = False
        self.mHasCookies = False
        self.mHasHeaders = False
        self.mSpiderName = None
        self.mSpiderClass = None
        self.mSpiderID = None
        self.mLogin = Login()
        self.mCookies = Cookies()
        self.mHeaders = Headers()
        self.mFilter = Filter()
        self.mLogic = Logic()
        self.read_config(config_xml)



    def read_config(self, config_xml):
        tree = ET.parse(config_xml)
        root = tree.getroot()
        for spider in root.iter('spider'):
            print(spider.tag, spider.attrib)
            self.mSpiderClass = spider.attrib['class']
            self.mSpiderID = spider.attrib['id']
            self.mSpiderName = spider.attrib['name']
            for item in spider.iter('item'):
                print(item.tag,item.attrib)
                if(item.attrib['name'] == 'login'):
                    self.mLogin.mName = 'login'
                    self.mLogin.mMethod = item.attrib['method']
                    self.mLogin.mUrl = item.attrib['url']
                    if('need' in item.attrib.keys()):
                        need = item.attrib['need']
                        if ( need == 'false'):
                            self.mLogin.mNeed = False
                        else:
                            self.mLogin.mNeed = True
                    else:
                        self.mLogin.mNeed = True
                    for field in item.iter('field'):
                        self.mLogin.mFields[field.attrib['name']] = field.text
                    print(self.mLogin.tostring())
                elif(item.attrib['name'] == 'cookies'):
                     if('need' in item.attrib.keys()):
                        need = item.attrib['need']
                        if ( need == 'false'):
                            self.mCookies.mNeed = False
                        else:
                            self.mCookies.mNeed = True
                     else:
                        self.mCookies.mNeed = True
                     for field in item.iter('field'):
                         self.mCookies.mFields[field.attrib['name']] = field.text
                     print(self.mCookies.tostring())

                elif(item.attrib['name'] == 'headers'):
                    if('need' in item.attrib.keys()):
                        need = item.attrib['need']
                        if ( need == 'false'):
                            self.mHeaders.mNeed = False
                        else:
                            self.mHeaders.mNeed = True
                    else:
                        self.mHeaders.mNeed = True
                    for field in item.iter('field'):
                         self.mHeaders.mFields[field.attrib['name']] = field.text
                    print(self.mHeaders.tostring())

                elif(item.attrib['name'] == 'filter' ):
                    if ('need' in item.attrib.keys()):
                        need = item.attrib['need']
                        if ( need == 'false' ):
                            self.mFilter.mNeed = False
                        else:
                            self.mFilter.mNeed = True
                    else:
                        self.mFilter.mNeed = True
                    for field in item.iter('field'):
                        self.mFilter.mFields[field.attrib['name']] = field.text
                    print(self.mFilter.tostring())

                elif(item.attrib['name'] == 'logic'):
                    if('need' in item.attrib.keys()):
                        need = item.attrib['need']
                        if (need == 'false'):
                            self.mLogic.mNeed = False
                        else:
                            self.mLogic.mNeed = True
                    else:
                        self.mLogic.mNeed = True
                    for field in item.iter('field'):
                        self.mLogic.mFields[field.attrib['name']] = field.text
                    print(self.mLogic.tostring())

                else:
                    print("error format",item.tag,item.attrib)





            return None
        #for item in root.findall("./item"):





    def get_postdata(self):
        return self.mPostdata

    def get_header(self):
        return self.mHeader

    def need_login(self):
        return self.mNeedlogin

    def has_cookies(self):
        return self.hasCookies

    def has_headers(self):
        return None


if __name__ == "__main__":
    config_bean = ConfigBean()
    config_bean.read_config("config.xml")




