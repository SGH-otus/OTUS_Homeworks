import time
import threading
import collections
import random

class MyCache_0:
    clear_timeout = 1
    timeout = 2
    size = 100
    cache = {}
    timestamps = {}
    lock = threading.Lock()
    
    def __init__(self, size=100, timeout=2):
        self.size = size
        self.timeout = timeout
        threading.Timer(self.clear_timeout, self.clear).start()
    
    def get(self, key):
        if key in self.cache:
            self.timestamps[key] = time.time()
            return self.cache[key]
        return None    
    
    def set(self, key, value):
        if len(self.cache) >= self.size:
            old_key = min(self.timestamps.keys(), key=lambda k:self.timestamps[k])
            self.cache.pop(old_key)
            self.timestamps.pop(old_key)
        self.cache[key] = value
        self.timestamps[key] = time.time()
        return
        
    def clear(self):
        t = time.time()
        self.lock.acquire()
        for k in self.timestamps.keys():
            if t - self.timestamps[k] >= self.timeout:
                del self.timestamps[k]
                del self.cache[k]
        self.lock.release()
        threading.Timer(self.clear_timeout, self.clear).start()
        return
 
class MyCache:
    clear_timeout = 1
    timeout = 2
    size = 100
    cache = {}
    timestamps = collections.OrderedDict()
    lock = threading.Lock()
    
    def __init__(self, size=100, timeout=2):
        self.size = size
        self.timeout = timeout
        threading.Timer(self.clear_timeout, self.clear).start()
    
    def get(self, key):
        if key in self.cache:
            self.lock.acquire()
            self.timestamps.pop(key)
            self.timestamps[key]= time.time()
            self.lock.release()
            return self.cache[key]
        return None    
    
    def set(self, key, value):
        self.lock.acquire()
        if len(self.cache) >= self.size:
            old = self.timestamps.popitem(last=False)
            self.cache.pop(old[0])
        self.cache[key] = value
        self.timestamps[key] = time.time()
        self.lock.release()
        return
        
    def clear(self):
        t = time.time()
        self.lock.acquire()
        for k in self.timestamps.keys():
            if (t - self.timestamps[k]) >= self.timeout:
                del self.timestamps[k]
                del self.cache[k]
        self.lock.release()
        threading.Timer(self.clear_timeout, self.clear).start()
        return
        
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print ('%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts))
        return result

    return timed
        
def testcache(Cache):
    @timeit
    def verify(cache):
        cache.set('test', 1)
        assert cache.get('test')
        
        for j in range(20):
            for i in range(10000):
                cache.set(i, i)

        for i in range(10000):
            cache.get(i)

    cache = Cache(200, 1)
    verify(cache)

# ===============TESTS 1===============
    
#testcache(MyCache)
#testcache(MyCache_0)

#exit(0)

# ===============TESTS 2===============

C = MyCache_0(20, 2)

for i in range(200):
    r = random.randint(1,100)
    C.set(r, r)
    time.sleep(random.randint(1, 5) / 5.0)
    print len(C.cache), C.cache

print
C = MyCache_0(20, 2)

for i in range(200):
    r = random.randint(1,100)
    C.set(r, r)
    time.sleep(random.randint(1, 5) / 50.0)
    print len(C.cache), C.cache











