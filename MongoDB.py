#!/bin/python
#coding=gbk

from DBAdapter import *
from pymongo import MongoClient


class MongoDB( DBAdapter ):

    def __int__(self,host,port,dbname,username,passwd):
        DBAdapter.__init__()
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
        return self.mDB[collectionname]

    def store(self,collection,data):
        self.insert(collection,data)
        return 0
        
    #---------------------KEY: 鏃堕棿鎴?------------------#
    #---------------url,timestamp,---------------------#
    def insert(self,collection,data):
        self.mDB.collection.insert(data)
        return 0
