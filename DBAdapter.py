#!/bin/python
#coding=gbk
import SimpleDB
class DBAdapter(SimpleDB):
    def __init__(self):
        SimpleDB.__init__(self)
        self.name="DBAdapter"

