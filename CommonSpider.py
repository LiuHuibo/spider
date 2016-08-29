#!/bin/python
#coding=gbk
import Spider
import urllib
import requests
import ConfigBean
import pprint


class CommonSpider(Spider):
    def __init__(self, configbean):
        Spider.__init__(self)
        self.mName = "CommonSpider"
        self.mConfigBean = configbean
        self.mHeaders = None
        self.mCookies = None
        self.mPostdata = None
        self.mSession = None
        self.mUrllogin = None
        self.mHomePage = None

    def set_cookies(self, cookies):
        self.mCookies = cookies
        return None

    def set_header(self, headers):
        self.mHeaders = headers
        return None

    def login_no_cookies(self):
        Spider.login()
        self.mPostdata = urllib.parse.urlencode(self.mConfigBean.get_postdata()).encode(encoding='utf-8')
        r = self.session.post(self.mUrllogin, data=self.mPostdata, headers=self.mHeaders)
        if r.json()['r'] == 1:
            print('Login Failed, reason is:')
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
                r = self.mSession.get(self.mHomePage, cookies=self.mCookies, verify=False)  # 实现验证码登陆
                print("r-->" + str(r.content))
        return True

    def login_use_cookies(self):
        pprint.pprint(dict(self.mCookies))
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

    def create_session(self):
        self.mSession = requests.session()

    def login(self):
        if self.mConfigBean.hasCookies():
            self.login_use_cookies()
        else:
            self.login_no_cookies()

    def crawl(self, url):
        self.mSession.get(url, cookies=self.mCookies, headers=self.mHeaders, verify=False)
        return None
