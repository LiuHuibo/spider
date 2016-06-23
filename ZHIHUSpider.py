#!usr/bin/python
#coding=utf8
import re
from collections import deque
try:
    # For Python 3.0 and later
    import urllib.parse
    import urllib.request
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

class ZHIHUSpider:
    def __init__(self):
        self.queue = deque()
        self.visited = set()
        self.url = "https://www.zhihu.com/"
        self.user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
        self.headers = { 'User-Agent' : self.user_agent }
        self.queue.append(self.url)

    def start(self):
        cnt = 0
        while self.queue:
            url = self.queue.popleft()
            self.visited |= {url}
            print("已经抓取:" + str(cnt) + "正在抓取--->" + url)
            cnt += 1
            req = urllib.request.Request(url,headers = self.headers)
            urlop = urllib.request.urlopen(req)
            if ("html" not in urlop.getheader("Content-Type")):
               continue
            #避免程序异常中止, 用try..catch处理异常
            try:    
                data = urlop.read().decode("utf-8")
            except:    
                continue

             #正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列  
            linkre = re.compile('href=\"(.+?)\"')  
            for x in linkre.findall(data):    
                if "http" in x and x not in self.visited:      
                    self.queue.append(x)      
                    print("加入队列:"+ x)