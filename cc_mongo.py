'mongodb 相关'

import pymongo,time,bson
import pymongo.errors
from concurrent import futures

mongo_dup_errors = pymongo.errors.BulkWriteError,pymongo.errors.DuplicateKeyError

def keys_to_projection(keys):
    return {key:True for key in keys}

def fetch_all_fields(co,field='_id',use_hint=False):
    ans = []
    ka = {}
    ka['projection'] = {field:True}
    if use_hint:
        ka['hint'] = [(field,1)]
    for doc in co.find(**ka):
        ans.append(doc[field])
    return ans

class async_co_helper:
    '辅助异步写入数据库'
    def __init__(self,co,batch_size=10000,tn=2):
        self.co = co
        self.docs = []
        self.pool = futures.ThreadPoolExecutor(tn)
        self.batch_size = batch_size
        self.count = 0

    def flush(self):
        '将缓存的文档写入数据库，非阻塞'
        if not self.docs:return
        self.pool.submit(self._insert_many,self.docs)
        self.docs = []

    def _insert_many(self,docs):
        try:
            self.co.insert_many(docs,ordered=False)
        except Exception as e:
            print(e)

    def insert(self,docs):
        '插入文档或文档列表，非阻塞，不一定立即写入'
        if isinstance(docs,dict):
            self.docs.append(docs)
            self.count += 1
        else:
            self.docs.extend(docs)
            self.count += len(docs)
        if len(self.docs) >= self.batch_size:
            self.flush()

    def create_index(self,*a,**k):
        self.pool.submit(self.co.create_index,*a,**k)

    def join(self):
        '等待数据库，阻塞'
        self.flush()
        self.pool.shutdown(wait=True)

    def queue_size(self):
        '返回当前等待的任务数量'
        return self.pool._work_queue.qsize()

    def wait(self,timesep=0.1,size_thr=3):
        '等待队列小一点，避免提交任务太多占用内存'
        while self.queue_size() >= size_thr:
            time.sleep(timesep)
