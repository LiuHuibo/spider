#!usr/bin/python
#coding=gbk
# URL�����������ù��˹�������ץȡ������URL
# URL�������������Ϲ���������ϴ�����URL
# ֪����վ�� ������ҳ�е�URL���ӣ�����������Ҫ�����ӻ����ֶ�---a. ä����Ч�ʽϵͣ�����ͨ����ǿ����b.������ȡ���Թ��򣬱���ĳ��ģʽ����ַ��
#             ������ӻ��ֶΣ���ȡhtml���ݴ洢�����ݿ�
#             ����xpath����������ʽ�����洢���������ݿ������
# 
from socket import * 
import struct
import ZHIHUSpider as zhihu
import json

spider = zhihu.ZHIHUSpider()
#��master��ȡurl =>request
def request_from_master(): 
    request_json = json.dumps({"ACTION":"GET","NUM":1})
    print("request from master:"+ request_json)
    tcpClientSock.send(bytes(request_json, 'utf-8'))  
    #recvdata = tcpClientSock.recv(BUFSIZ)  
    # if(not recvdata):
    #   return None  
    #print(str(recvdata, encoding='utf-8')) 
    #
    recvdata_res = tcpClientSock.recv(BUFSIZ)  
    if(not recvdata_res):
       return None  
    recv_json = json.loads(str(recvdata_res, encoding='utf-8'))
    urls = None
    if(recv_json["RETCODE"] == 0):
        urls = recv_json["URLS"]
    print(str(recv_json))
    return urls
#������ǰURL����ȡ����URL
def extract_urls(current_url):
    next_url = spider.geturlids(current_url)
    print("current_url's flowers and flowees is -----> " + str(next_url))
    return next_url
#�洢��ǰURL��WEB���ݵ�mongodb
def store(current_url):
    print("store:"+str(current_url))
    return 0
#��url���鷢�͵�master��������POST
def send_to_master(to_send):
    post_json = json.dumps({"ACTION":"POST","URLS": to_send })
    print("send to master:"+post_json)
    length = len(post_json)
    print("length is " +str(length))
    tcpClientSock.send(bytes(post_json,'utf-8'))  
    return 0

spider.create_session_nologin_()
HOST = 'localhost'  
PORT = 5008
BUFSIZ = 40960  
ADDR = (HOST, PORT)  
tcpClientSock = socket(AF_INET, SOCK_STREAM)  
tcpClientSock.connect(ADDR)  
while(True):
    urls = request_from_master()
    if (not urls):
        break   
    #��ȡģ��
    current_url = urls
    current_home_url = spider.get_home_url(current_url)
    current_hmtl = spider.gethtml(current_home_url)
    to_send = []
    for next_url in extract_urls(current_url):
        to_send.append(next_url)
        print("next_url--->"+next_url)
    store(current_hmtl)
    send_to_master(to_send)
tcpClientSock.close()  
