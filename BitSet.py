#!/bin/python
# -*- conding: gbk -*-

import array


class BitSet(object):
    def __init__(self, capacity):
        #"B"类型相当于 C 语言的 unsigned char， 即占用1byte（8位），所以size大小设置为8
        self.unit_size = 8
        self.unit_count = int((capacity + self.unit_size - 1) / self.unit_size)
        self.capacity = capacity
        self.arr = array.array("B", [0] * self.unit_count)

    def any(self):


    def all(self):

    def none(self):

    def count(self):

    def size(self):

    def get(self, pos):

    def test(self, pos):

    def set(self, pos = -1):

    def reset(self, pos = -1):

    def flip(self, pos = -1):

    def binstr(self):

