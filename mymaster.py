#!usr/bin/python
#coding=gbk
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
import RedisQueue as RQ
HOST = 'localhost'
PORT = 5008
BUFSIZ = 40960
ADDR = (HOST, PORT)
# main
#global distributed_queue
global bf
redis_queue = RQ.RedisQueue('master')
redis_queue.put("https://www.zhihu.com/people/alex-liu-90-89/followees")

#distributed_queue.put("https://www.zhihu.com/people/alex-liu-90-89/followees")
bf = BFilter.BloomFilter()


def run_proc(name,serverSock,clientSock,buffersize=40960):
    serverSock.close()
    time.sleep(3)
    print('Run child process %s (%s)...' % (name, os.getpid()))
    while (True):
        json_data = get_from_slave(clientSock, buffersize)
        #print(str(json_data))
        request = json_data["ACTION"]
        if (request == 'GET'):
            #print("GO TO GET")
            if (redis_queue.qsize() > 0):
                num = json_data["NUM"]
                send(clientSock, redis_queue.get())
                #print("get url ok")
            else:
                print("get url fail")
        elif (request == 'POST'):
            urls = json_data["URLS"]
            for url in urls:
                if ( not bf.is_contaions(url)):
                    redis_queue.put(url)
                    #print("put url ok---- " + str(url))
        else:
            print("Error Input")
            clientSock.close()
            break
    sys.exit(0)


def get_from_slave(tcpClientSock,buffersize):
    data = tcpClientSock.recv(buffersize)
    if(data == None):
       return None
    strdata = str(data, encoding='utf-8')
    #print("receive from slave--->"+strdata)
    json_data = json.loads(str(data, encoding='utf-8'))
    #tcpClientSock.send(bytes('[%s]%s'%(time.ctime(), str(data, encoding='utf-8')), 'utf-8'))
    #tcpClientSock.send(bytes('[%s]%s'%(time.ctime(), str(data, encoding='utf-8')), 'utf-8'))
    #data解析，格式 GET|POST:{CONTENT}
    return json_data

def send(tcpClientSock,item):
    json_data = json.dumps({"RETCODE":0,"URLS":item})
    #print("send to slave--->"+json_data)
    tcpClientSock.send(bytes(json_data, 'utf-8'))
    return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='myapp.log',
                        filemode='w')
    logging.debug('This is debug message')
    logging.info('This is info message')
    logging.warning('This is warning message')

    #
    print("begin build socket....")
    tcpServSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tcpServSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServSock.bind(ADDR)
    tcpServSock.listen(5)
    id = 0
    while (True):
        print('waiting for connection...')
        (tcpClientSock, addr) = tcpServSock.accept()
        print('...connected from: ', addr)
        id = id +1
        p = Process(name="myService"+ str(id), target=run_proc, args=("process connect", tcpServSock, tcpClientSock, BUFSIZ))
        print("BEFORE:", p, p.is_alive())
        p.start()
        tcpClientSock.close()
        print('DURING:', p, p.is_alive())
        #*******************join 会阻塞父进程，等待子进程返回**************************
        #****************类似于waitpid()，去掉后会导致僵尸进程************************
        #1.join方法的作用是阻塞主进程（挡住，无法执行join以后的语句），专注执行多线程。
        #2.多线程多join的情况下，依次执行各线程的join方法，前头一个结束了才能执行后面一个。
        #3.无参数，则等待到该线程结束，才开始执行下一个线程的join。
        #4.设置参数后，则等待该线程这么长时间就不管它了（而该线程并没有结束）。不管的意思就是可以执行后面的主进程了。
        #p.join()

    tcpServSock.close()









