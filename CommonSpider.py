#!/bin/python
#coding=gbk
import Spider as Sp
import urllib
import requests
import ConfigBean
import pprint


class CommonSpider(Sp.Spider):
    def __init__(self):
        Sp.Spider.__init__(self)
        print("CommonSpider init")
        self.mName = "CommonSpider"
        self.mConfigBean = None
        self.mHeaders = None
        self.mCookies = None
        self.mFilter = None
        self.mReqData = None
        self.mSession = None
        self.mUrllogin = None
        self.mHomePage = None
        self.mPostdata = None
        self.action = dict()

    def set_postdata(self, postdata):
        self.mPostdata = urllib.parse.urlencode(postdata).encode(encoding='utf-8')

    def set_homepage(self, url):
         self.mHomePage = url

    def set_cookies(self, cookies):
        self.mCookies = cookies

    def set_header(self, headers):
        self.mHeaders = {
            'Connection':"keep-alive",
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Host':'www.zhihu.com',
            'Upgrade-Insecure-Requests':'1'
            }
        self.mHeaders = headers
        pprint.pprint(dict(self.mHeaders))
        return None

    def set_filter(self, filter):
        self.mFilter = filter

    def config_from_bean(self, configbean):
        self.mConfigBean = configbean
        print("cookies.mFields is",configbean.mCookies.mFields)
        self.set_cookies(configbean.mCookies.mFields)
        self.set_header(configbean.mHeaders.mFields)
        self.set_filter(configbean.mFilter.mFields)
        self.set_homepage(configbean.mLogin.mUrl)
        self.set_postdata(configbean.mLogin.mFields)

    def login_no_cookies(self):
        r = self.session.post(self.mUrllogin, data=self.mPostdata, headers=self.mHeaders)
        if r.json()['r'] == 1:
            print('Login Failed, reason is:')
            for m in r.json()['data']:
                print(r.json()['data'][m])
            print('So we use cookies to login in...')
            has_cookies = False
            for key in self.mCookies:
                if key != '__name__' and self.mCookies[key] != '':
                    has_cookies = True
                    break
            if has_cookies is False:
                raise ValueError('请填写config.ini文件中的cookies项.')
            else:
                r = self.mSession.get(self.mHomePage, cookies=self.mCookies, verify=False)  # 实现验证码登陆
                print("r-->" + str(r.content))
        return True

    def login_use_cookies(self):
        print("*************longin_use_cookies********************")
        print(self.mHomePage)
        pprint.pprint(dict(self.mCookies))
        pprint.pprint(dict(self.mCookies))
        pprint.pprint(dict(self.mHeaders))
        r = self.mSession.get(self.mHomePage, cookies=self.mCookies, headers=self.mHeaders, verify=False)   # 实现验证码登陆
        #print("r.ending:"+r.encoding)
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
             print("************************HomePage*********************")
             #print("r-->" + (r.content).decode("gbk", 'ignore'))
             return  r.status_code
        else:
            return -1

    def create_session(self):
        requests.packages.urllib3.disable_warnings()
        self.mSession = requests.session()

    def login(self):
        if self.mConfigBean.hasCookies():
            self.login_use_cookies()
        else:
            self.login_no_cookies()

    def crawl(self, url):
        r = self.mSession.get(url, cookies=self.mCookies, headers=self.mHeaders, verify=False)
        if (r != None):
            print("**************Crwal Result:"+url+"*********************")
            #print("r-->"+ (r.content).decode("gbk",'ignore'))
            #print("r-->" + (r.content).decode(r.encoding,'ignore'))
            return (r.content).decode(r.encoding,'ignore')
        else:
            return None

    def crawl(self, url, handler_function = None, ** handlerargs):
        result = None
        r = self.mSession.get(url, cookies=self.mCookies, headers=self.mHeaders, verify=False)
        if (r != None):
            print("**************Crwal Result:"+url+"*********************")
            if (handler_function  != None):
                result = handler_function(r,** handler_function)
            else:
                result = (r.content).decode(r.encoding,'ignore')
            return result
        else:
            return None



