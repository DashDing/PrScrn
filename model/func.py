# -*- coding: utf-8 -*-
#function
import config
import html2text
import urllib
import chardet
import json
from classes import DBHelper
from config import *

#探测网页的编码方式
def detectEncoding(response):
    encodingHeaders = response.headers.encoding
    encodingChardet = detectStrEncoding(response.body)
    if not encodingChardet is None:
        return encodingChardet
    elif not encodingHeaders is None:
        return encodingHeaders
    else:
        return config.defaultCoding
    #return response.headers.encoding or config.defaultCoding

def detectStrEncoding(str):
    encoding = chardet.detect(str).get('encoding')
    if encoding is None:
        encoding = 'utf-8'
    return encoding

#html文件转换为字符串
#参数为html的内容
def html2string(decodedHtml):
    converter = html2text.HTML2Text()
    converter.ignore_links = True
    string = converter.handle(decodedHtml)
    return string

#从mysql数据表中获得一定的内容
#table为数据表的名字，wait判断条件，limit为结果数量
def getTarget(table = 'url_table', wait = 2, limit = 1):
    target = []
    dbhelper = DBHelper()
    data = dbhelper.oncesql("select url from {0} where wait = {1} limit {2}".format(table, wait, limit))
    if data:
        for item in data:
            target.append(item[0])
    del dbhelper
    return target

#删除URl中的HTTP、HTTPS
#url参数为URL
def rmHttpHttps(url):
	url = url.replace("https://",'')
	url = url.replace("http://",'')
	return url

#测试模式
#alert为输出信息
def testModePrint(alert):
    if config.testMode:
        print alert

#将链接相对路径转换为绝对路径
#link位链接、url为域名
def convertLink(link, url):
    reLink = ""
    if link.startswith('http'):
        reLink = link
    elif link.startswith('//'):
        reLink = 'http:'+link
    elif link.startswith('./'):
        if url.endswith('/'):
            reLink = url + link[2:len(link)]
        else:
            reLink = url.split('/')
            if len(reLink) <= 3:
                reLink = url + '/' + link[2:len(link)]
            else:
                reLink = '/'.join(reLink[0:len(reLink)-1]) + '/' + link[2:len(link)]
    elif link.startswith('/'):
        reLink = '/'.join(url.split('/')[0:3]) + link
    elif link.startswith('../'):
        reLink = url.split('/')
        relink = link.split('../')
        reLink = '/'.join(reLink[0:len(reLink)-len(relink)]) + "/" + relink[-1]
    else:
        if url.endswith('/'):
            reLink = url + link
        else:
            reLink = url.split('/')
            if len(reLink) <= 3:
                reLink = url + '/' + link
            else:
                reLink = '/'.join(reLink[0:len(reLink)-1]) + '/' + link
    
    return reLink

#print convertLink('123/ibm.img','http://www.baidu.com/obs/ios/eee/123')



def solr_search(solr = 'torPage',field = '*', hl_simple_post = "<-1>", hl_simple_pre = "<-1>", wt = 'json', hl = 'off', q = '*', rows = 10000,hl_maxAlternateFieldLength = 100):
    url = 'http://localhost:8983/solr/{0}/select?hl.fl={1}&hl.simple.pre={2}&hl.simple.post={3}&hl={4}&q={5}&rows={6}&wt={7}&hl.maxAlternateFieldLength={8}'.format(solr, field, hl_simple_pre, hl_simple_post, hl, q, rows, wt, hl_maxAlternateFieldLength)
    response = urllib.urlopen(url)
    data_response = json.loads(response.read())
    data = data_response.get('response',{'docs':None}).get('docs')
    data_hl = data_response.get('highlighting',None)
    if not data_hl is None and not data is None:
        for i in data:
            if not data_hl[i['id']].get('content',None) is None:
                i['content']=data_hl[i['id']]['content'][0]
    return data

#2017 03 06 ding
#生成tor client 配置文件
def make_torrc(torrcFilePath = 'torrc_auto_first', cachePath = '/home/data/tor', nickname = 'ding', socksPortList = str(defaultTorProxyForScanner)):
    output = open(torrcFilePath,'w')
    otherOptionList = ['ClientTransportPlugin obfs3 exec /usr/bin/obfsproxy managed\n',\
                       'DataDirectory {0}\n'.format(cachePath),\
                       'TruncateLogFile 1\n',\
                       'Log notice file {0}/notice.log\n'.format(cachePath),\
                       'Nickname {0}\n'.format(nickname),\
                       'UseBridges 1\n',\
                       'bridge obfs3 192.36.31.162:50435 098019752AF71024DF42D086356623DF542452E4\n',\
                       'bridge obfs3 192.36.31.132:53471 0B391BA3753C1B492BC1188A25C283F86290A77B\n',\
                       'bridge obfs3 54.218.44.158:40872 86831E15228C540C24713E5CDAA8C7F5BF8B9544\n',\
                       'ExitPolicy reject *:*\n',\
                       'ContactInfo Ding@test\n']
    if '-' in socksPortList:
        ran = socksPortList.split('-')
        begin = int(ran[0]) if not ran[0] is None else 9060
        end = int(ran[1]) if not ran[1] is None else begin
        for port in range(begin, end):
            otherOptionList.append('SocksPort {0}\n'.format(port))
    else:
            otherOptionList.append('SocksPort {0}\n'.format(socksPortList))

    output.writelines(otherOptionList)
    output.close()

#2017 03 06 ding
#退出
def signal_handler(signal, frame):
    print '[*] Ctrl + C is pressed'
    global to_exit
    to_exit = True

#def solr_update(solr = 'torPage',strUpdate())

#2017 07 03 ding
#increase per day
def increase_statistic():
    #select
    db = DBHelper()
    sql = 'select count(id) from domain_table group by year(first_find_time),month(first_find_time),day(first_find_time)'
    result = db.oncesql(sql)
    counts = [int(a[0]) for a in result]


    #draw pic
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 8))
    plt.plot(range(len(counts)), counts, 'blue')
    plt.show()

def url2filename(url):
    import  hashlib
    path = htmlPath
    filename = hashlib.md5(bytes(url.encode(defaultCoding))).hexdigest()+'default.html'
    return path+filename
