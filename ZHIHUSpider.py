#!usr/bin/python
#coding=utf8
import re
from collections import deque
import urllib
import socket
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
        self.url_base = "https://www.zhihu.com/people"
        self.url_login_info="https://www.zhihu.com"
        self.url_id="kaifulee"
        self.url_followees_suffix="followees"
        self.url_followers_suffix="followers"
        self.url_about_suffix="about"
        self.user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
        self.headers = { 'User-Agent' : self.user_agent }
        self.queue.append(self.url_id)

        self.url_login="http://www.zhihu.com/login/email"
        self.email="fly8421@outlook.com"
        self.passwd="33614793"
        self.captcha_type="cn"
        self.remember_me="true"
        self._xsrf= None
        self.post = None

        #_xsrf=0e55d862d9d880808a8e93c01c4a7368&password=123456&captcha_type=cn&remember_me=true&email=fly8421%40outlook.com
        #self.cookie = cookielib.LWPCookieJar()
        #self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
    def getLoginPara(self):
        reqLogin = urllib.request.Request(self.url_login_info,headers = self.headers)
        try:
            urloplogin = urllib.request.urlopen(reqLogin)
        except:
            print("主页访问异常")
            return None

        if ("html" not in urloplogin.getheader("Content-Type")):
            print("头部异常")
            return None

        try:
            data = urloplogin.read().decode("utf-8")
            print(data)
        except:
            print("解码异常")
            return None

        searchObj = re.search( r'<input type="hidden" name="_xsrf" value="(.+?)"/>', data, re.M|re.I)
        if searchObj:
            print ("search --> searchObj.group(1) : ", searchObj.group(1))
            return searchObj.group(1)
        else:
            print ("Nothing Found！")
            return None


    #登录知乎
    def login(self):

        self._xsrf = self.getLoginPara()
        if(self._xsrf == None):
            return None
        self.post= {
            '_xsrf':self._xsrf,
            'password':self.passwd,
            'captcha_type':self.captcha_type,
            'remember_me':self.remember_me,
            'email':self.email
        }

        self.post_data = urllib.parse.urlencode(self.post).encode(encoding='UTF8')
        req = urllib.request.Request(self.url_login, self.post_data, self.headers)
        response = urllib.request.urlopen(req)
        result = response.read().decode("utf-8")
        return result

    def getFolloweesUrl(self, urlid):
        url=self.url_base+"/"+urlid+"/"+self.url_followees_suffix
       
        return (url)

    def getFollowersUrl(self, urlid):
        url=self.url_base+"/"+urlid+"/"+self.url_followers_suffix
        print("url-->"+url)
        return (url)

    def getAboutUrl(self,urlid):
        url=self.url_base+"/"+urlid+"/"+self.url_about_suffix
        return (url)

    #需要先登录：获取被关注的人
    def addFollowers(self,urlid):
        reqfollowers = urllib.request.Request(self.getFollowersUrl(urlid), headers = self.headers)
        try:
            urlopfollowers = urllib.request.urlopen(reqfollowers)
        except:
            print("页面打开异常")
            return -1

        if ("html" not in urlopfollowers.getheader("Content-Type")):
            print("头部异常")
            return -2
            #避免程序异常中止, 用try..catch处理异常
        try:    
            data = urlopfollowers.read().decode("utf-8")
            print(data)
        except:
            print("解码异常") 
            return -3
             #正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列  
        linkrefollowers = re.compile(r"href=\"https://www.zhihu.com/people/(.+?)\"") 
        for x in linkrefollowers.findall(data):    
            if x not in self.visited:      
               self.queue.append(x)      
               print("加入队列:"+ x)
        return 0

    #需要先登录：获取关注的人
    def addFollowees(self,urlid):
        reqfollowees = urllib.request.Request(self.getFolloweesUrl(urlid), headers = self.headers)
        try:
            urlopfollowees = urllib.request.urlopen(reqfollowees)
        except:
            print("页面打开异常")
            return -1

        if ("html" not in urlopfollowees.getheader("Content-Type")):
            print("头部异常")
            return -2
        #避免程序异常中止, 用try..catch处理异常
        try:    
            data = urlopfollowees.read().decode("utf-8")
        except:    
            print("解码异常")  
            return -3

         #正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列  
        linkrefollowees = re.compile(r"href=\"https://www.zhihu.com/people/(.+?)\"")  
        for x in linkrefollowees.findall(data):    
            if  x not in self.visited:      
                self.queue.append(x)      
                print("加入队列:"+ x)

        return 0


    def start(self):
        result = self.login()
        if( result == None):
            print("登录失败")
            print("登录返回报文："+ result)

        cnt = 0
        while self.queue:
            urlid = self.queue.popleft()
            self.visited |= {urlid}
            print("已经抓取:" + str(cnt) + "正在抓取--->" + urlid)
            cnt += 1
            #reqabout = urllib.request.Request(self.getAboutUrl(urlid), headers = self.headers)
            if self.addFollowers(urlid) < 0 :
                continue
            if self.addFollowees(urlid) < 0 :
                continue




            




