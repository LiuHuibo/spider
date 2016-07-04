#!usr/bin/python
#coding=UTF-8
import re
import urllib
import socket
import http.cookiejar
import json
import gzip
import configparser
import requests
import pprint
import collections 
#import localcookies


try:
    # For Python 3.0 and later
    import urllib.parse
    import urllib.request
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

def ungzip(data):
    try:        # 尝试解压
        print('正在解压.....')
        data=gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data

class ZHIHUSpider:
    def __init__(self):
        self.queue = collections.deque()
        self.visited = set()
        self.url_base = "https://www.zhihu.com/people"
        self.url_login_info="https://www.zhihu.com"
        self.url_id="kaifulee"
        self.url_followees_suffix="followees"
        self.url_followers_suffix="followers"
        self.url_about_suffix="about"
        self.user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
        #self.headers = { 'User-Agent' : self.user_agent }
        self.headers = {
            'Connection':'keep-alive',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Host':'www.zhihu.com',
            'Upgrade-Insecure-Requests':1
            }
        self.queue.append(self.url_id)
        self.captcha_pre="https://www.zhihu.com/captcha.gif?r="
        self.url_login="http://www.zhihu.com/login/email"
        self.email="fly8421@outlook.com"
        self.passwd="123456"
        self.captcha_type="cn"
        self.remember_me="true"
        self._xsrf= None
        self.post = None
        self.cookies = None
        self.cj = http.cookiejar.CookieJar()
        self.session = None
        #self.cookies = http.cookiejar.CookieJar()
        #self.opener  = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))
        #self.opener.addheaders = [('User-agent', 'Opera/9.23')]
        #self.opener.addheaders = self.headers
        #urllib.request.install_opener(self.opener)






        #_xsrf=0e55d862d9d880808a8e93c01c4a7368&password=123456&captcha_type=cn&remember_me=true&email=fly8421%40outlook.com
        #self.cookies = cookielib.LWPCookieJar()
        #self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookies)

    #get captcha
    def read_config(self):
        section_re = re.compile(r"^\s*\[([^\s]+?)\]\s*$") 
        item_re=re.compile(r"^\s*([^\s]+?)\s*=\s*([^\s]+?)\s*$") 
        section = None
        item_name = None
        item_value = None
        d1 = collections.defaultdict(list)
        d  = collections.defaultdict(list)
        flag = 0
        f = open("config.ini")
        for  line in  f.readlines(): 
            #print("line is-->" + line)
            secobj = section_re.match(line)
            if secobj:
                if(flag == 0):
                    flag = 1
                    section = secobj.group(1)
                else :
                    d1[section].append(d)
                    #print(section+"此时seciton的内容-->")
                    list(d.items())
                    d = collections.defaultdict(list)
                    section = secobj.group(1)
                #print("匹配到section:"+section)
                continue

            itemobj = item_re.match(line)
            if itemobj:
                item_name = itemobj.group(1)
                item_value = itemobj.group(2)
                d[item_name].append(item_value)
                #print("item_name:"+item_name+",item_value:"+item_value)

        f.close()
        d1[section].append(d)
        print("all info from config.ini")
        for key1,value1 in d1.items():
            print(key1,value1)

        cf = d1
        self.cookies = collections.defaultdict(list)(d1.items["cookie"])
        info_config = collections.defaultdict(list)(d1.items["info"])
        self.email = info_config.get("email")
        self.passwd = info_config.get("passwd")
        #self._xsrf = info_config.get("_xsrf")

    def read_config_parser(self):
        cf = configparser.ConfigParser()
        cf.read('config.ini')
        cookie_config = cf.items('cookie')
        self.cookies = dict(cookie_config)
        self.email = cf.get('info','email')
        self.passwd = cf.get('info','passwd')
        #self._xsrf = cf.get('cookie','_xsrf')


    def read_chrome_cookie(self):
        self.cookies=localcookies.get_chrome_cookies(".zhihu.com")

    def get_captcha(self):
        captchaurl = captcha_pre + str(int(time.time()*1000))+"&type=login"
        #1467455728504&type=login"
        print(captchaurl)

        return captcha
    def getLoginPara(self):

        try:
            urloplogin = self.opener.open(self.url_login_info)
        except:
            print("主页访问异常")
            return None

        if ("html" not in urloplogin.getheader("Content-Type")):
            print("头部异常")
            return None

        # for item in self.cookies:
        #     print('Name = ' + item.name)
        #     print('Value = ' + item.value)
        #     if(item.name == "_xsrf"):
        #         self._xsrf = item.value
        # return self._xsrf

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
        print("_xsrf--->"+self._xsrf)
        if(self._xsrf == None):
            return None
        self.post= {
            '_xsrf':self._xsrf,
            'password':self.passwd,
            'captcha_type':self.captcha_type,
            'remember_me':self.remember_me,
            'email':self.email
        }

        self.post_data = urllib.parse.urlencode(self.post).encode(encoding='utf-8')
        response = self.opener.open(self.url_login, self.post_data)
        #response = urllib.request.urlopen(req)
        
        #
        #response = urllib.request.urlopen(req)
        #response = self.opener.open(req)

        #data = response.read()
        #data = ungzip(data).decode("utf-8")
        #print(data)
        print("response-->"+response.read().decode("utf-8"))
        result = str(response.info())
        print("response.info-->>" + result)


        # print("result-->"+result)
        # result2 = response.geturl()
        # print("result2:"+result2)
        # print("code:"+str(response.getcode()))
        # print("info:"+str(response.info()))
        # data = json.dumps(str(response.info()))
        # print("python原始数据:"+repr(data))
        # print("python对象"+data)
        # dir(response)
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


    def create_session(self):
        self.read_config()
        #self.read_chrome_cookie()
        #pprint(self.cookies)
        print("self.email-->"+self.email)
        print("self.passwd-->"+self.passwd)
        session = requests.session()
        self.post= {
            '_xsrf':self._xsrf,
            'password':self.passwd,
            'captcha_type':self.captcha_type,
            'remember_me':self.remember_me,
            'email':self.email
        }
        self.post_data = urllib.parse.urlencode(self.post).encode(encoding='utf-8')
        r = session.post(self.url_login, data=self.post_data, headers=self.headers)
        #print("r-->"+r)
        if r.json()['r'] == 1:
            print ('Login Failed, reason is:')
            for m in r.json()['data']:
                print(r.json()['data'][m])
            print('So we use cookies to login in...')
            has_cookies = False
            for key in self.cookies:
                if key != '__name__' and self.cookies[key] != '':
                    has_cookies = True
                    break
        if has_cookies is False:
            raise ValueError('请填写config.ini文件中的cookies项.')
        else:
            # r = requests.get('http://www.zhihu.com/login/email', cookies=cookies) # 实现验证码登陆
            r = session.get('http://www.zhihu.com/login/email', cookies=self.cookies,verify=False) # 实现验证码登陆
            print("r-->"+str(r.content))

        #self.post_data = urllib.parse.urlencode(self.post).encode(encoding='utf-8')
        #response = self.opener.open(self.url_login, self.post_data)
        #response = urllib.request.urlopen(req)

    def create_session_nologin(self):
        self.read_config_parser()
        #for k in self.cookies.keys():
            #self.cj.add_header([(k,self.cookies(k))])

        self.opener  = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        header = []
        for key, value in self.headers.items():
            elem = (key, value)
            header.append(elem)
        self.opener.addheaders=header
        #for k in self.headers.keys():
            #self.opener.addheaders = [(k, self.headers[k])]

        for k in self.cookies.keys():
            cookiename = k
            cookievalue = self.cookies[k]
            self.opener.addheaders.append(('Cookie', cookiename+'='+cookievalue))

        urllib.request.install_opener(self.opener)
        req=urllib.request.Request("http://www.zhihu.com")

        content=self.opener.open(req)

        response = ungzip(content.read()).decode("utf-8")
        for item in self.cj:
             print('Name = ' + item.name)
             print('Value = ' + item.value)

        print("response.info-->>" + response)


    def create_session_nologin_(self):
        self.read_config_parser()
        #self.read_chrome_cookie()
        pprint.pprint(dict(self.cookies))
        print("self.email-->"+self.email)
        print("self.passwd-->"+self.passwd)
        self.session = requests.session()
        r = self.session.get('http://www.zhihu.com', cookies=self.cookies,headers=self.headers,verify=False) # 实现验证码登陆
        print("r.ending:"+r.encoding)
        #r.encoding='utf-8'
        #先用requests默认的编码方式解码r.content,解码后编码成"utf-8"
        #data为bytes直接输出中文为数字字符的形势，故需要解码成gbk格式
        #UnicodeEncodeError: 'gbk' codec can't encode character '\u2022' in position 29215: illegal multibyte sequence
        #表明打印的时候需要自动转为gbk编码
        #因此可以简化为下面的一步即可：
        #注意：bytes会自动编码为unicode('utf-8')
        #不要直接用str对bytes进行转换，中文字符会变成编码格式
        # if( r != None ):
        #     print("status code:"+str(r.status_code))
        #     data = ((r.content).decode(r.encoding)).encode("utf-8")
        #     print("r-->"+ data.decode("gbk",'ignore'))
        if( r != None ):
             print("status code:"+str(r.status_code))
             print("r-->"+ (r.content).decode("gbk",'ignore'))

        #需要先登录：获取被关注的人
    def addFollowers_(self,urlid):
        r = self.session.get(self.getFollowersUrl(urlid), cookies=self.cookies,headers = self.headers,verify = False)
        if( r != None ):
             print("status code:"+str(r.status_code))
             print("抓取错误")
             #print("r-->"+ (r.content).decode("gbk",'ignore'))
        else:
            return -1
         #正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列  
        linkrefollowers = re.compile(r"href=\"https://www.zhihu.com/people/(.+?)\"") 
        for x in linkrefollowers.findall((r.content).decode("gbk",'ignore')):    
            if x not in self.visited:      
               self.queue.append(x)      
               print("加入队列:"+ x)
        return 0

    #需要先登录：获取关注的人
    def addFollowees_(self,urlid):
        r = self.session.get(self.getFolloweesUrl(urlid),cookies=self.cookies, headers = self.headers,verify = False)
        if( r != None ):
             print("status code:"+str(r.status_code))
             #print("r-->"+ (r.content).decode("gbk",'ignore'))
        else:
            print("抓取错误")
            return -1
         #正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列  
        linkrefollowees = re.compile(r"href=\"https://www.zhihu.com/people/(.+?)\"")  
        for x in linkrefollowees.findall((r.content).decode("gbk",'ignore')):    
            if  x not in self.visited:      
                self.queue.append(x)      
                print("加入队列:"+ x)

        return 0


    def start(self):
        self.create_session_nologin_()
        cnt = 0
        while self.queue:
             urlid = self.queue.popleft()
             self.visited |= {urlid}
             print("已经抓取:" + str(cnt) + "正在抓取--->" + urlid)
             cnt += 1
             if self.addFollowers_(urlid) < 0 :
                 continue
             if self.addFollowees_(urlid) < 0 :
                 continue




            




