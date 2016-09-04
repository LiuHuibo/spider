#!/bin/python
#coding=gbk
from pymongo import MongoClient
import random
class MongoDB:
    def __int__(self,host,port,dbname,username,passwd):
        self.mName = "MongoDB"
        self.mHost = host
        self.mPort = port
        self.mUserName = username
        self.mPasswd = passwd
        self.mDbname = dbname
        self.mClient = MongoClient(self.mHost, self.mPort)
        self.mDB = None
    def conn(self):
        self.mDB = self.mClient[self.mDbname]
    def get_collection(self,collectionname):
        return  self.mDB[collectionname]
    def store(self,html):
        return  0
