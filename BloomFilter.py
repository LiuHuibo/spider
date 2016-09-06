#!/bin/python
# _*_coding:utf_8_
import BitSet
import os
import sys


class SimpleHash():
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter():
    def __init__(self, BIT_SIZE=1 << 25):
        self.BIT_SIZE = 1 << 25
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.bitset = BitSet.BitSet(self.BIT_SIZE)
        self.hashFunc = []

        for i in range(len(self.seeds)):
            self.hashFunc.append(SimpleHash(self.BIT_SIZE, self.seeds[i]))

    def put(self, value):
        for f in self.hashFunc:
            loc = f.hash(value)
            self.bitset.set(loc)

    def is_contaions(self, value):
        if value == None:
            return False
        ret = True
        for f in self.hashFunc:
            loc = f.hash(value)
            ret = ret & self.bitset.get(loc)
        return ret


if __name__ == '__main__':
    fd = open("urls.txt")
    bloomfilter = BloomFilter()
    while True:
        # url = raw_input()
        url = fd.readline()
        if (url == 'exit'):
            # if url is equal exit break
            break
        if not bloomfilter.is_contaions(url):
            bloomfilter.put(url)
        else:
            print
            'url :%s has exist' % url

