#!/bin/python
#coding=gbk
import configparser


class ConfigBean:
    def __init__(self, configfile):
         self.mName = None
         self.mPostdata = None
         self.mHeader = None
         self.mNeedlogin = False
         self.mHasCookies = False
         self.mHasHeaders = False

    def read_config(self, configfile):
        cf = configparser.ConfigParser()
        cf.read('config.ini')
        cookie_config = cf.items('cookies')
        self.cookies = dict(cookie_config)
        return None

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

