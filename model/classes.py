# -*- coding: utf-8 -*-
import MySQLdb
import config
import socks
import threading
from random import choice
from time import sleep
from config import defaultTorProxyForScanner, defaultPortScanRange,priorPort,proxyPort,Localhost,User,Password,Database

#class to maintain tor proxy pool
class TorProxyPool:

    proxyPool = []

    def __init__(self):
        try:
            ipPool = proxyPort.split(';')
            if not ipPool is None:
                for ipItem in ipPool :
                    if not ipItem in '':
                        ipAndPorts = ipItem.split(':')
                        ip = ipAndPorts[0]
                        ports = ipAndPorts[1]
                        ports = ports.split(',')
                        for item in ports:
                            if '-' in item: 
                                ran = item.split('-')
                                for port in range(int(ran[0]),int(ran[1])+1):
                                    self.proxyPool.append('http://{0}:{1}'.format(ip,port))
                            else:
                                self.proxyPool.append('http://{0}:{1}'.format(ip,item))

        except:
            self.proxyPool = []

    def __del__(self):
        self.proxyPool = None
        del self.proxyPool

    #get a random tor proxy
    def getProxy(self):
        return choice(self.proxyPool)

#class to control mySql database
#last modefied in 2017 03 12
class DBHelper:

    conn = None
    def __init__(self):
        if self.conn is None:
            self.conn = MySQLdb.connect(Localhost,User,Password,Database)

    def __del__(self):
        if not self.conn is None:
            self.conn.close()
            self.conn = None

    #excute an sql, return 0 for success, -1 for failed
    def dosql(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
        except:
            self.conn.rollback()
        finally:
            self.conn.commit()

    #query ,return data list
    def select(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        return data

    #do query or excute once
    def oncesql(self,sql):
        data = None
        if 'select' in sql or 'SELECT' in sql:
            data = self.select(sql)
        else:
            data = self.dosql(sql)
        return data

#2017 03 13
class Scanner:
    #parameter
    proxyPort = []
    proxyAddress = ''
    unScanPortList = []
    destination = ''
    maxFailed = 0
    maxThread = 1

    #class value
    failedCount = 0
    threadingList = []
    threadingResult = []

    def __init__(self, proxyPort = str(defaultTorProxyForScanner), unScanPortList = [], destination = '', maxFailed = 1, proxyAddress = '127.0.0.1',maxThread = 1):
        self.unScanPortList = unScanPortList
        self.destination = destination
        self.maxFailed = maxFailed
        self.proxyAddress = proxyAddress
        if '-' in proxyPort:
            ports = proxyPort.split('-')
            start = int(ports[0]) if not ports[0] is None else 9060
            end = int(ports[1]) if not ports[1] is None else start
            for port in range(start, end):
                self.proxyPort.append(port)
        else:
            self.proxyPort.append(int(proxyPort))
        self.maxThread = len(self.proxyPort) if len(self.proxyPort) > 1 else 1


    def process_soccks5_error(self, e, port):
        if e.value[0] == config.SOCKS_DESC_UNAVAILABLE:
            print "DESC_UNAVAILABLE/NO_INTROS", port
        elif e.value[0] in [config.SOCKS_CANT_ATTACH, config.SOCKS_TTL_EXPIRED]:
            print "CANT_ATTACH/TTL_EXPIRED", port
        elif (e.value[0] in [config.SOCKS_REFUSED_CONN_BY_RULE, config.SOCKS_REFUSED_CONN_REMOTE]):
            print "DESC_HERE/PORT_CLOSED", port
        elif (e.value[0] == config.SOCKS_TOR_MISC):
            print "DESC_HERE/PORT_FILTERED", port
        elif (e.value[0] == config.SOCKS_HOST_UNREACHABLE):
            print "SOCKS_HOST_UNREACHABLE", port
        else:
            print "CONN_FAILED/UKNOWN_REASON", " ", e.value[0], " ", port

    def make_connect(self, port):
        socket = socks.socksocket()
        socket.setproxy(socks.PROXY_TYPE_SOCKS5, self.proxyAddress,choice(self.proxyPort))
        finished = -1
        try:
            socket.connect((self.destination, port))
            print "DESC_HERE/OPEN ", str(port)
            self.threadingResult.append(port)
            self.failedCount = 0
            finished = 1
        except socks.Socks5Error as e:
            self.process_soccks5_error(e, port)
            if (e.value[0] == config.SOCKS_HOST_UNREACHABLE):
                self.failedCount += 1
            else:
                self.failedCount = 0
        finally:
            socket.close()
            if finished:
                return port
            return 0

    def scann(self):
        #任务来自preScan | portScan'python portScan.py -d {0} -p {1} -r {2}'.format(destination, 9050,'0-65535'
        if '-' in self.unScanPortList:
            ran = self.unScanPortList.split('-')
            start = int(ran[0]) if not ran[0] is None else 1024
            end = int(ran[1]) if not ran[1] is None else 65535
            for port in priorPort:
                if port>= start and port <= end:
                    # 是否开启新的线程
                    if len(self.threadingList) < self.maxThread:
                        t = threading.Thread(target=self.make_connect, \
                                             args=[port], \
                                             name='make_connect--{0}:{1}'.format(self.destination, port))
                        self.threadingList.append(t)
                        t.setDaemon(True)
                        t.start()
                    # 维护线程池
                    for t in self.threadingList:
                        if not t.isAlive():
                            self.threadingList.remove(t)
                    # 是否已经有结果
                    if len(self.threadingResult) > 0:
                        return self.threadingResult[0]
                    sleep(1)

            for p in range(start,end):
                if not p in priorPort:
                    #是否开启新的线程
                    if len(self.threadingList) < self.maxThread:
                        t = threading.Thread(target=self.make_connect, \
                                             args=[p], \
                                             name='make_connect--{0}:{1}'.format(self.destination, p))
                        self.threadingList.append(t)
                        t.setDaemon(True)
                        t.start()
                    #维护线程池
                    for t in self.threadingList:
                        if not t.isAlive():
                            self.threadingList.remove(t)
                    #是否已经有结果
                    if len(self.threadingResult) > 0:
                        return self.threadingResult[0]
                    sleep(1)
            return -1
        else:
            #处理所有待处理端口
            for port in self.unScanPortList:
                #是否开启新的线程
                if len(self.threadingList) < self.maxThread:
                    t = threading.Thread(target=self.make_connect, \
                                         args=[port], \
                                         name='make_connect--{0}:{1}'.format(self.destination, port))
                    self.threadingList.append(t)
                    t.setDaemon(True)
                    t.start()
                #维护线程池
                for t in self.threadingList:
                    if not t.isAlive():
                        self.threadingList.remove(t)
                #是否已经有结果
                if len(self.threadingResult) > 0:
                    return self.threadingResult[0]
                sleep(1)
            return -1

