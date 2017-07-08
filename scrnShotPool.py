#encoding:utf-8
from multiprocessing import Pool
from model.classes import DBHelper
from model.func import url2filename
from prscrn import take_scrnshot
from time import sleep
import os

PROCESSNUM = 5
filepath = '/home/jssec/Desktop/scrnshot/{}.png'

class ScrnShotPool:

    def __init__(self,test_mode = False):
        self.test_mode = test_mode
        self.db = DBHelper()
        self.idle = True

    def get_task(self):
        self.idle = False
        if self.db is None:
            self.db = DBHelper()
        sql = 'select id,url,wait from domain_table where status = 1 and wait < 8 and wait %8 >=4 limit 100'
        tasks = self.db.oncesql(sql)
        self.tasks = tasks

    def update(self,id,wait):
        if self.db is None:
            self.db = DBHelper()
        wait = wait|8
        sql = 'update domain_table set wait = {} where id = {}'.format(wait,id)
        self.db.oncesql(sql)

    def run(self):

        if len(self.tasks) <= 0:
            print 'there is no task. exit!'
            return
        self.idle = False
        pool = Pool(processes=PROCESSNUM)
        for [id,url,wait] in self.tasks:
            self.update(id,wait)
            filename = url2filename(url)
            if not os.path.exists(filename):
                continue
            result = pool.apply_async(take_scrnshot, (filename,filepath.format(id),self.test_mode))

        pool.close()
        pool.join()
        if result.successful():
            print 'all tasks have been finished. exit!'
            self.idle = True
        else:
            print 'some errors have been accured!'


    def isIdle(self):
        return self.idle

if __name__ == '__main__':

    scp = ScrnShotPool(test_mode=True)
    count = 0
    while True and count <= 5:
        if scp.isIdle():
            scp.get_task()
            scp.run()
        sleep(30)
        print count
        count += 1
        break