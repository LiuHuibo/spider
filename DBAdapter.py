#!/bin/python
#coding=gbk
import SimpleDB
class DBAdapter:
    def __init__(self,db):
        db.__init__(self)
        self.name="DBAdapter"
    def store(self,xml):
        return 0


