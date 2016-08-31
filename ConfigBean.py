#!/bin/python
#coding=gbk
import configparser
import xml.etree.ElementTree as ET


class Login:

    def __init__(self):
        self.mName = None
        self.mMethod = None
        self.mNeed = False
        self.mFields = dict()

    def to_string(self):
        print(self.mName, self.mMethod, self.mNeed)
        print(self.mFields)


class ConfigBean:
    def __init__(self):
        self.mPostdata = None
        self.mHeader = None
        self.mNeedlogin = False
        self.mHasCookies = False
        self.mHasHeaders = False
        self.mSpiderName = None
        self.mSpiderClass = None
        self.mSpiderID = None
        self.mLogin = Login()
        self.mCookies = None
        self.mHeaders = None
        self.mFilter = None
        self.mLogic = None



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
                    self.mLogin.to_string()
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




