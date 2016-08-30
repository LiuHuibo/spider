#!/bin/python
#coding=gbk
import configparser
import xml.etree.ElementTree as ET


class ConfigBean:
    def __init__(self, configfile):
         self.mName = None
         self.mPostdata = None
         self.mHeader = None
         self.mNeedlogin = False
         self.mHasCookies = False
         self.mHasHeaders = False

    def read_config(self, config_xml):
        tree = ET.parse(config_xml)
        root = tree.getroot()
        for spider in root.iter('spider'):


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
        return self.hasHeaders

