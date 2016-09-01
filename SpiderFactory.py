#!/bin/python
#coding=gbk
import Spider
import  CommonSpider
import ConfigBean


class SpiderFactory:
    def __init__(self, configfile):
        self.config_bean = ConfigBean.ConfigBean(configfile)
    def getSpider(self):
        spider = None
        if(self.config_bean.mSpiderClass == 'CommonSpider'):
            spider = CommonSpider.CommonSpider
            spider.__init__(self.config_bean)
        else:
            spider = None
        return  spider



