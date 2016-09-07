#!usr/bin/python
#coding=gbk
# URL�����������ù��˹�������ץȡ������URL
# URL�������������Ϲ���������ϴ�����URL
# ֪����վ�� ������ҳ�е�URL���ӣ�����������Ҫ�����ӻ����ֶ�---a. ä����Ч�ʽϵͣ�����ͨ����ǿ����b.������ȡ���Թ��򣬱���ĳ��ģʽ����ַ��
#             ������ӻ��ֶΣ���ȡhtml���ݴ洢�����ݿ�
#             ����xpath����������ʽ�����洢���������ݿ������
#

import SpiderFactory
import Parser
import DBAdapter
import MongoDB
import Comm
import traceback
from datetime import *
import json
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
        # ��ȡģ��
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
            
            now = datetime.now()
            time = now.isoformat()
            spidername = spider.get_name()
            url = current_html
            param = ''
            method = 'get'
            title = ''
            html = current_html
            data = {"time":time, "spidername":spidername, "url":url, 
                    "param":param,"method":method, "title":title,"html":html}
            json_data = json.dumps(data)

            dbadapter.store("zhihu.com",json_data)
            comm.send_to_master(to_send)
    comm.close()




