#!/bin/python
#coding='gbk
from socket import *
import json


class Comm:

    def __init__(self,host,port,bufsize):
        self.mHost = host
        self.mPort = port
        self.mBufsize = bufsize
        self.mTcpClientSock = None

    def conn_to_master(self):
        ADDR = (self.mHost, self.mPort)
        self.mTcpClientSock = socket(AF_INET, SOCK_STREAM)
        self.mTcpClientSock.connect(ADDR)

        # 从master获取url =>request
    def request_from_master(self,num):
        request_json = json.dumps({"ACTION": "GET", "NUM": num})
        print("request from master:" + request_json)
        self.mTcpClientSock.send(bytes(request_json, 'utf-8'))
        # recvdata = tcpClientSock.recv(BUFSIZ)
        # if(not recvdata):
        #   return None
        # print(str(recvdata, encoding='utf-8'))
        #
        recvdata_res = self.mTcpClientSock.recv(self.mBufsize)
        if (not recvdata_res):
            return None
        recv_json = json.loads(str(recvdata_res, encoding='utf-8'))
        urls = None
        if (recv_json["RETCODE"] == 0):
            urls = recv_json["URLS"]
        print(str(recv_json))
        return urls

    # 将url数组发送到master服务器，POST
    def send_to_master(self,to_send):
        post_json = json.dumps({"ACTION": "POST", "URLS": to_send})
        print("send to master:" + post_json)
        length = len(post_json)
        print("length is " + str(length))
        self.mTcpClientSock.send(bytes(post_json, 'utf-8'))
        return 0

    def close(self):
        self.mTcpClientSock.close()

