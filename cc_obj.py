'python 对象相关'

import os,sys,pickle,zlib,time,threading,queue

is_in_idle = 'pythonw' in sys.executable

_DATA_PATH = 'datas'

def set_data_path(path:str):
    global _DATA_PATH
    _DATA_PATH = path

def get_data_path():
    return _DATA_PATH

def join_data_path(*fn):
    return os.path.join(_DATA_PATH,*fn)

def save_obj(obj,fn:str,compress=False):
    fn = join_data_path(fn)
    b = pickle.dumps(obj)
    if compress:
        b = zlib.compress(b)
    with open(fn,'wb') as f:
        f.write(b)

def load_obj(fn:str,compress=False):
    fn = join_data_path(fn)
    with open(fn,'rb') as f:
        b = f.read()
    if compress:
        b = zlib.decompress(b)
    return pickle.loads(b)

def list_to_inv(d):
    return {x:i for i,x in enumerate(d)}

def split_list(d:list,step=100000):
    n = len(d)
    for i in range(0,n,step):
        yield d[i:i+step]

def split_iter(it,step=1000):
    da = []
    for obj in it:
        da.append(obj)
        if len(da) >= step:
            yield da
            da = []
    if da:
        yield da

class async_iter_wrapper:
    def __init__(self,it,batch_size=1000,timesep=0.1,size_thr=10):
        self.batch_size = batch_size
        self.timesep = timesep
        self.size_thr = size_thr
        self.it = it
        self.q = queue.Queue()
        t = threading.Thread(target=self._th)
        t.start()

    def _th(self):
        da = []
        for d in self.it:
            da.append(d)
            if len(da) < self.batch_size:continue
            self.q.put(da)
            da = []
            while self.q.qsize() >= self.size_thr:
                time.sleep(self.timesep)
        if da:
            self.q.put(da)
        del da
        self.q.put(None)

    def __iter__(self):
        while True:
            da = self.q.get()
            if da is None:return
            yield from da
