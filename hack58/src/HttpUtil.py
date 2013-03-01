#coding=utf-8
import urllib2
import cookielib
import HTMLParser
import time
import traceback


class HttpUtil():
    def __init__(self,proxy = None):
        #proxy = {'http': 'http://210.14.143.53:7620'}
        if proxy != None:
            proxy_handler = urllib2.ProxyHandler(proxy)
            self.opener = urllib2.build_opener(proxy_handler,urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        else:
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

        self.opener.addheaders=[('User-agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322)')]

    def GetUrlContent(self,url,times=1):
        for i in range(times):
            try:
                return self.opener.open(url).read()
            except:
                time.sleep(1)
                print traceback.format_exc()
                continue
        
        return None
    
    def Post(self,url,data,times=1):
        for i in range(times):
            try:
                return self.opener.open(url,data).read()
            except:
                time.sleep(1)
                print traceback.format_exc()
                continue
        return None
if __name__ =='__main__':
    httpUtil = HttpUtil()
    print httpUtil.GetUrlContent('http://i1.dpfile.com/2006-03-19/26616_m.jpg')