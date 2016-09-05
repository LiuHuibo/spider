#!usr/bin/python
#coding=gbk
# URL过滤器，设置过滤规则，用来抓取待爬的URL
# URL组合器，设置组合规则，用来组合待爬的URL
# 知乎网站： 过滤网页中的URL连接，仅仅保留需要的链接或者字段---a. 盲爬（效率较低，但是通用性强）。b.设置爬取策略规则，比如某个模式的网址。
#             组合连接或字段，获取html内容存储到数据库
#             利用xpath或者正则表达式分析存储到本地数据库的内容
#

import SpiderFactory
import Parser
import DBAdapter
import MongoDB
import Comm
import traceback
if __name__ == "__main__":

    dbadapter = DBAdapter.DBAdapter(MongoDB.MongoDB)

    spiderFactory = SpiderFactory.SpiderFactory("config.xml")
    spider = spiderFactory.get_spider()
    spider.create_session()
    spider.login_use_cookies()

    parser = Parser.Parser()

    comm = Comm.Comm('localhost',5008,40960)
    comm.conn_to_master()

    while (True):
        current_url = comm.request_from_master(1)
        if (not current_url):
            break
        # 爬取模块
        try:
            current_html = spider.crawl(current_url)
        except:
            print("crawl exception")
            continue
        to_send = []

        next_urls = parser.extract_urls(current_html)
        if (next_urls):
            for next_url in next_urls:
                to_send.append(next_url)
                print("next_url--->" + next_url)
            dbadapter.store(current_html)
            comm.send_to_master(to_send)
    comm.close()




