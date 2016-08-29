#!usr/bin/python
#coding=UTF-8
import collections
class DistributedQueue:
    def __init__(self):
        self.queue = collections.deque()

    def get(self):
        return self.queue.popleft()

    def put(self,item):
        self.queue.append(item)
        

    def size(self):
        return len(self.queue)


