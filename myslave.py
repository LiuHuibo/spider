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
            dbadapter.store(current_html)
            comm.send_to_master(to_send)
    comm.close()




