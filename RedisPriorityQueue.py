import redis


class RedisPriorityQueue(ojbect):
    
    def __init__(self, name, namespace='queue', **redis_kwargs):
        pass
    
    def qsize(self):
        pass

    def empty(self):
        pass

    def put(self, item):
        pass

    def get(self, block=True, timeout=None):
        pass

    def get_nowait(self):
        pass

if __name__ == '__main__':
    q = RedisPriorityQueue('test')
    q.put('hello world')
    print(q.get())    
