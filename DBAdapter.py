#!/bin/python
#coding=gbk
import SimpleDB


class DBAdapter:
    def __init__(self,db):
        db.__init__(self)
        self.name="DBAdapter"

    def store(self,  name, data):
        db.store(name, data)
        return 0

    def acquire(self, key):
        return 0

