from Spider import *
from CommonSpider import *


class LianjiaSpider(CommonSpider):

    def __init__(self):
        CommonSpider.__init__(self)

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
