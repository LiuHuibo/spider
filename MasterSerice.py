#!usr/bin/python
#coding=UTF-8
import socket
import sys
import time
import DistributedQueue as DistQ
import BloomFilter as BFilter
import struct
import json
import os
import time
from multiprocessing import Process
import logging
HOST = 'localhost'
PORT = 5008
BUFSIZ = 40960
ADDR = (HOST, PORT)
# main
global distributed_queue
global bf
distributed_queue = DistQ.DistributedQueue()

distributed_queue.put("alex-liu-90-89")
bf = BFilter.BloomFilter()
class MasterServer:
    def __init__(self, host, port, max_connections=5, bufsize=40960):
        self.mHost = host
        self.mPort = port
        self.mBufSize = bufsize
        self.mAddress = (self.mHost, self.mPort)
        self.mDistQueue = DistQ.DistributedQueue()
        self.mDistQueue.put("alex-liu-90-89")
        self.mBf = BFilter.BloomFilter()
        self.mTcpServSock = None
        self.mTcpClientSock = None
        self.mMaxConnections = max_connections

    def run(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='myapp.log',
                            filemode='w')
        logging.debug('This is debug message')
        logging.info('This is info message')
        logging.warning('This is warning message')
        print("begin build socket....")
        self.mTcpServSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mTcpServSock.bind(ADDR)
        self.mTcpServSock.listen(self.mMaxConnections)
        while (True):
            print('waiting for connection...')
            (self.mTcpClientSock, addr) = self.mTcpServSock.accept()
            print('...connected from: ', addr)
            p = Process(name="myService", target=run_proc, args=("process connect",
                                                                 self.mTcpServSock,
                                                                 self.mTcpClientSock,
                                                                 self.mBufSize,
                                                                 self.mBufSize))
            print("BEFORE:", p, p.is_alive())
            p.start()
            tcpClientSock.close()
            print('DURING:', p, p.is_alive())
            p.join()
        self.mTcpServSock.close()