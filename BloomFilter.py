#!/bin/python
#conding='gbk'
class BloomFilter:
    def __init__(self,m,n,k,f):
        self.mM = 512
        self.mN = 
        self.mK =   
        self.mF = 
        self.visited = set()


    def put(self,item):
        if item not in self.visited:
            self.visited.add(item)
            return 0
        else:
            return -1

