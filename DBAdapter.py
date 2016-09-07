#!/bin/python
#coding=gbk
import SimpleDB


class DBAdapter:
    def __init__(self):
        self.name = "DBAdapter"
    def conn(self):
        pass
    def dis_connect(self):
        pass
    def commit(self):
        pass
    def rollback(self):
        pass
    def store(self, table, data):
        pass
    def acquire(self, key):
        pass

