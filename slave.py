#!usr/bin/python
#coding=UTF-8
# URL过滤器，设置过滤规则，用来抓取待爬的URL
# URL组合器，设置组合规则，用来组合待爬的URL
# 知乎网站： 过滤网页中的URL连接，仅仅保留需要的链接或者字段---a. 盲爬（效率较低，但是通用性强）。b.设置爬取策略规则，比如某个模式的网址。
#             组合连接或字段，获取html内容存储到数据库
#             利用xpath或者正则表达式分析存储到本地数据库的内容
# 
from socket import * 
import struct
import ZHIHUSpider as zhihu
import json

spider = zhihu.ZHIHUSpider()
#从master获取url =>request
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
#解析当前URL，获取其中URL
def extract_urls(current_url):
    next_url = spider.geturlids(current_url)
    print("current_url's flowers and flowees is -----> " + str(next_url))
    return next_url
#存储当前URL的WEB内容到mongodb
def store(current_url):
    print("store:"+str(current_url))
    return 0
#将url数组发送到master服务器，POST
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
    #爬取模块
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
