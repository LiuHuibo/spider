#!/bin/python
#coding=gbk
import Spider
import CommonSpider as CS
import ConfigBean as CB


class SpiderFactory:
    def __init__(self, configfile):
        self.config_bean = CB.ConfigBean(configfile)

    def get_spider(self):
        if (self.config_bean.mSpiderClass == 'CommonSpider'):
            commonSpider = CS.CommonSpider()
            commonSpider.config_from_bean(self.config_bean)
            return commonSpider
        else:
            return None

if __name__ == "__main__":
    spiderFactory = SpiderFactory("config.xml")
    spider = spiderFactory.get_spider()
    spider.create_session()
    spider.login_use_cookies()
    spider.crawl("https://www.zhihu.com/topic/19681246/hot")





