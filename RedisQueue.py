#!/bin/python
#coding='gbk'
import redis
class RedisQueue(object):
    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace='queue', **redis_kwargs):
        self.mDb = redis.Redis(**redis_kwargs)
        self.mKey = '%s:%s' % (namespace, name)

    def qsize(self)：
        return self.mDb.llen(self.mKey)

    def empty(self):
        return self.qsize == 0

    def put(self, item):
        self.mDb.rpush(self.mKey, item)

    def get(self, block=True, timeout=None):
        if block:
            item = self.mDb.blpop(self.mKey, timeout = timeout)
        else:
            item = self.mDb.lpop(self.mKey)
        if item:
            item = item[1]
        return item

    def get_nowait(self):
        return self.get(False)

if __name__ == '__main__':
    q = RedisQueue('test')
    q.put('hello world')
    q.get()