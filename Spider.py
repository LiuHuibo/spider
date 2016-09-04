#!/bin/python
#coding=gbk
class Spider:
    def __init__(self):
        print("Spider init")
        self.mName = "Spider"

    def config_from_bean(self, configbean):
        return None

    def login(self):
        return None

    def read_config(self):
        return None

    def write_config(self):
        return None

    def create_session(self):
        return None

    def login_no_cookies(self):
        return None

    def login_use_cookies(self):
        return None

    def crawl(self,url, callback = None):
        return None
