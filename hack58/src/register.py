from HttpUtil import HttpUtil
from lxml import etree
import urllib2
from urllib2 import urlopen
from urllib import urlencode
import time
import random

#proxy_handler = urllib2.ProxyHandler({'http': 'http://211.167.112.16:82'})
#opener = urllib2.build_opener(proxy_handler)
#urllib2.install_opener(opener)

g_HttpUtil = HttpUtil()
g_SuccessFile = 'result.txt'
g_ProxyFile = 'proxy.txt'
g_ProxyIt = 0
g_ProxyList = []

with open(g_ProxyFile) as f:
    lines = f.readlines()
    g_ProxyList = [{'http':'http://' + line.strip()} for line in lines]


def randomStr(l):
    ret = ''
    for i in xrange(l):
        ret += chr(ord('a') + random.randint(0,25))
    return ret

def GenerateAccount():
    for i in xrange(100000):
        base = randomStr(10)
        ret = {}
        ret['nickName'] = base
        ret['txtemail'] = base + '@163.com'
        ret['password'] = base + '_'
        yield ret

def GetProxy():
    global g_ProxyIt
    if g_ProxyIt >= len(g_ProxyList):
        return None
    g_ProxyIt += 1
    print g_ProxyList[g_ProxyIt-1]
    return g_ProxyList[g_ProxyIt-1]

def RecordSuccess(account):
    with open(g_SuccessFile,'a') as f:
        f.write(account['nickName'] + ' ' + account['txtemail'] +' '+ account['password'] + '\n')

def write2file(content,filename):
    with open(filename,'w') as f:
        f.write(content)



def Register(account):
    try:
        html = g_HttpUtil.GetUrlContent('http://passport.58.com/reg/')
        #write2file(html,'1.html')
        tree = etree.HTML(html)
        account['ptk'] = tree.xpath('//input[@id="ptk"]/@value')[0]
        account['cd'] = tree.xpath('//input[@id="cd"]/@value')[0]
        #ret = urlopen('http://passport.58.com/save', urlencode(account))    
        content = g_HttpUtil.Post('http://passport.58.com/save', urlencode(account)) 
        if content.find('/regok?regok=1') == -1:
            write2file(content, 'error.txt')
            return None
        return account
    except:
        return None



def main():
    failNum = 0
    global g_HttpUtil
    g_HttpUtil = HttpUtil(GetProxy())
    for account in GenerateAccount():
        ret = Register(account)
        if ret == None:
            print 'failed:',account['nickName']
            failNum += 1
            #consecutive failure 5 times,berak
            if failNum >= 5:
                proxy = GetProxy()
                if proxy == None:
                    break
                g_HttpUtil = HttpUtil(proxy)
                failNum = 0
            continue
        print 'success:',ret['nickName']
        RecordSuccess(ret)
        failNum = 0
        time.sleep(1)



if __name__ == '__main__':
    main()