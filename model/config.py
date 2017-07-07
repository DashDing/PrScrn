# -*- coding: utf-8 -*-
#addtional config

import os

#mysql数据库配置
Localhost = '223.3.92.185' #2017-02-13 10:16 ding
Password  = 'ibmc51'
User      = 'root'
Database  = 'TorSearchProj'

#mysql数据表名称
DomainTable = 'domain_table'
YellowPageTable = 'yelloPage_table'
DomainHashTable = 'domain_hash'
ResourceHashTable = 'resource_hash'
BlackTable = 'black_table' #2017 02 03 ding
#2017 03 07 ding
NoportTable = 'noport_table'

#redis配置
RedisHost = '223.3.92.185'
RedisPort = 6379

#html文件存储路径
#htmlPath = "/var/www/html/"
htmlPath = "/home/jssec/Desktop/html/"
#url to test Tor client to network
#testHttp = 'http://3g2upl4pq6kufc4m.onion'
testUrl = 'http://www.baidu.com/'

#默认编码格式
defaultCoding = 'utf-8'

#solr配置
solrCore = 'torPage' 
solrConnection = 'http://223.3.83.136:8983/solr/'+solrCore
#正则表达式
patternOnionAddress = '((http|https):\/\/)?(([abcdefghigklmnopqrstuvwxyz234567]|[^\.\:\/1890\#\@\%\$]){16}(\.onion)+(:\d*)?)'
patternDomain = '[abcdefghigklmnopqrstuvwxyz234567]{16}(\.onion)+'
patternOnionAddressIndex = 2

#代理池
#proxyPort = "127.0.0.1:8123-8125,8126;"
proxyPort = "127.0.0.1:8123;"

#是否跟随
followStra = False
onionSpiderTimeOut = 80
onionSpiderDelay = 0.5

#时间格式
timeFormatYMD = '%Y-%m-%d'
timeFormatYMDX = '%Y-%m-%d %X'

#是否测试模式
testMode = False

#爬虫名字
onionspider = 'onionspider'
resourcespider = 'resourcespider'
domainspider = 'domainspider'
yellowpagespider = 'yellowpagespider'
searchEnginespider = 'searchenginespider'
baiduspider = 'baiduspider'
bingspider = 'bingspider'
searchSpiderList = [searchEnginespider,baiduspider,bingspider]

#hash表的level对应的扫描间隔
hashTableLeveltoInteval = [600,6000,60000,600000]
hashTableMaxLevel = 3

#处理的特殊状态码
handleSuccessCode = [200, 204, 205 ,206]
handleStrictCode = [401,403]
handleErrorCode = [500, 502, 503, 504, 400, 404, 408, 301]
handleRedirectCode = [300, 302, 307]

#item的字段
itemUrl = 'url'
itemTitle = 'title'
itemContent = 'content'
itemResources = 'resources'
itemLinks = 'links'
itemTotalLinks = 'totalLinks'

#各个爬虫使用的redis列表的key
redisKeyPrefix = 'TorCrawler:'
redisKeyofOnionSpider = redisKeyPrefix + 'unCrawledUrls'
redisKeyofResourcesSpider = redisKeyPrefix + 'recourcesUrls'
redisKeyofDomainSpider = redisKeyPrefix + 'unCrawledNormalUrls'
redisKeyofYellowSpider = redisKeyPrefix + 'yellowPageUrls'
redisKeyofSearchEngineSpider = redisKeyPrefix + 'searchEngineUrls'
redisKeyofBaiduSpider = redisKeyPrefix + 'baiduUrls'
redisKeyofBingSpider = redisKeyPrefix + 'bingUrls'
#2017 03 13 ding
#test redis key
redisKeyofTest = redisKeyPrefix + 'test'
redisKeyofAnnounced = redisKeyPrefix + 'announced'

#onionspider爬取的资源文件的链接
resourcesPattern = '//img/@src|//link/@href|//embed/@src|//video/@src'

#快照是否存储资源文件
isDownloadResources = False
#资源文件存储路径
resrcPath = os.getcwd()+"/resource/"

#搜索引擎前缀
startPagePrefix = "https://www.startpage.com/do/search?cmd=process_search&language=english&enginecount=1&pl=&abp=1&cdm=&tss=1&ff=&theme=&prf=464341bcfbcf47b736ff43307aef287a&suggestOn=1&flag_ac=0&lui=english&cat=web&query="
searchEngineSpiderDelay = 2
baiduPrefix = 'http://www.baidu.com/s?ie=utf-8&wd='
baiduSpiderDelay = 2
bingPrefix = 'http://cn.bing.com/search?go=搜索&q='
bingSpiderDelay = 2


#黄页识别标准
yellowpageidentifyrate = 0.0
yellowpageIdentifytotal = 400

#doman_table fields
domainTableID = 'id'
domainTableURL = 'url'
domainTableWait = 'wait'
domainTableSearch = 'search_result'
domainTableFirstFindTime = 'first_find_time'
domainTableLastUpTime = 'last_up_time'
domainTableStatus = 'status'
domainTableLanguage = 'lan'
domainTablecal = 'cal'
domainTableLastModifyTime = 'last_modify_time'
domainTableSource = 'src'
domainTableIsStrict = 'is_strict'

#domian_hash fields
domainHashID = 'id'
domainHashURL = 'url'
domainHashTime = 'time'
domainHashLevel = 'level'

#resource_hash fields
resourcesHashID= 'id'
resourcesHashURL = 'url'
resourcesHashTime = 'time'
resourcesHashLevel = 'level'

#yellowPage_table fields
yellowPageTableID = 'id'
yellowPageTableURL = 'url'
yellowPageTableWait = 'wait'
yellowPageTableHash = 'hash'
yellowPageTableLastAccess = 'last_access'
yellowPageTableAddTime = 'add_time'
yellowPageTableLevel = 'level'

#pageTable fields
pageTableID = 'id'
pageTableURL = 'url'
pageTableTitle = 'title'
pageTableDomain = 'domain'
pageTableLastModifyTime = 'last_modify_time'
pageTableSnapshot = 'snapshot'
pageTableContentHash = 'content_hash'
pageTableTextContent = 'text_content'
pageTableResource = 'resource'
PageTableRefer = 'refer'

#2017-02-13 10:16 ding
#black_table fields
blackTableID = "id"
blackTableDomain = 'domain'
blackTableTime = 'time'
blackList = []

#2017 03 15 ding
noportTableURL = 'url'

#2017 03 06 ding
#socks特殊状态
SOCKS_CANT_ATTACH = 1
SOCKS_REFUSED_CONN_BY_RULE = 2
SOCKS_HOST_UNREACHABLE = 4
SOCKS_REFUSED_CONN_REMOTE  = 5
SOCKS_TTL_EXPIRED = 6
SOCKS_DESC_UNAVAILABLE = 10
SOCKS_TOR_MISC = 12

#2017 03 06 ding
#preScan程序配置
popularWEBPort = [80, 443, 4050, 8080]
defaultTorProxyForScanner = 9060
maxTargetPoolForPreScan = 10
#2017 03 07 ding
#torScan程序配置
TOR_NUM = 1
CLIENT_NUM = 1
BEGIN_TOR_PORT = 10200
PORT_PERTOR = 25
#portScan配置
defaultPortScanRange = '1024-65535'
popularNoWEBPort = [6667,11009,55080]
maxFailedForPortScan = 1000
#Scanner
priorPort = popularWEBPort + popularNoWEBPort