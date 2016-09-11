#!/bin/python
#coding=gbk

from DBAdapter import *
from pymongo import MongoClient


class MongoDB(DBAdapter):

    def __init__(self, host, port, **optionsdic):

        DBAdapter.__init__(self, host, port, **optionsdic)
        self.mName = "MongoDB"
        self.mHost = host
        self.mPort = port
        self.mUserName = optionsdic['username']
        self.mPasswd = optionsdic['passwd']
        self.mDbname = optionsdic['dbname']
        self.mClient = None
        self.mDB = None

    def conn(self):
        self.mClient = MongoClient(self.mHost, self.mPort)
        self.mDB = self.mClient[self.mDbname]

    def commit(self):
        pass

    def rollback(self):
        pass

    def store(self, collection, data):
        print(type(data))
        if isinstance(data, dict):
            print("dict")
            return self.insert_one(collection, data)
        elif isinstance(data, list):
            print('list')
            return self.insert_batch(collection, data)
        else:
            return  None

    def query(self, collection, key ):
        return self.mDB[collection].find_one(key)


    def fetch_all(self, collection, key ):
        collection = self.mDB[collection]
        result = []
        for item in collection.find(key):
            result.append(item)
        return  result

    def fetch_one(self, collection, key):
        collection = self.mDB[collection]
        result = collection.find_one(key)
        return  result


    def update(self,collection, key):
        self.mDB[collection].update()

    def get_collection(self, collection):
        return self.mDB[collection]

    def insert_one(self, collection, data):
        result = self.mDB[collection].insert_one(data)
        id = result.inserted_id
        return id

    def insert_batch(self, collection, data):
        result = self.mDB[collection].insert_many(data)
        ids = result.inserted_ids
        return  ids

    def execmd(self,cmd):
        result = self.mDB.cmd
        return result.inserted_ids



if __name__ == "__main__":
   optionsdic = {'dbname':'testdb','username':'liuhb','passwd':'123456'}
   mongodb = MongoDB('localhost', 27017, **optionsdic)
   mongodb.conn()
   data = {
       "time": "2014",
       "url": "www.baidu.com",
       "param": "",
       "method": "get",
       "title": "test",
       "html": "wwwwwwwwwwww"
   }
   mongodb.store('zhihu', data)

