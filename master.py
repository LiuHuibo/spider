#!usr/bin/python
#coding=UTF-8
distributed_queue = DistributedQueue()
bf = BloomFilter()

initial_pages = "www.renmingribao.com"

while(True):
    if request == 'GET':
        if distributed_queue.size()>0:
            send(distributed_queue.get())
        else:
            break
    elif request == 'POST':
        bf.put(request.url)
        