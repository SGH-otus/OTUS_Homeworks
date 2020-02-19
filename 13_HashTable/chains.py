import random
import string
import time
import sys

def GenRandStr(str_len):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(str_len))

class HashTable:
    table = []
    Pearson_Table = []
    dim = 2
     
    class Elem:
        key = None
        val = None
        next = None

        def __init__(self, key, val): 
            self.key = key
            self.val = val
     
    def __init__(self, size):
        self.table = [None] * size
        self.Pearson_Table = range(256)
        random.shuffle(self.Pearson_Table)
    
    def HashFunc(self, val):
        key = [0] * self.dim
        for i in range(self.dim):
            k = self.Pearson_Table[(ord(val[0]) + i) % 256]
            for c in val:
                k = self.Pearson_Table[k ^ ord(c)]  
            key[i] = k
        
        r = 0
        for i in range(self.dim):
            r = (r << 8) + key[i]
        
        return r
    
    def AddVal(self, val):
        key = self.HashFunc(val)
        new_e = self.Elem(key, val)
        e = self.table[key]

        if e is not None:
            while e.next != None:
                e = e.next
            e.next = new_e
        else:
            self.table[key] = new_e
        return
        
    def FindVal(self, val):
        key = self.HashFunc(val)
        e = self.table[key]
        
        if (e is None):
            return None
        elif (e.val == val):
            return val
        else:
            while e.next != None:
                e = e.next
                if e.val == val:
                    return val
        return None
     
    def DelVal(self, val):
        key = self.HashFunc(val)
        e = self.table[key]
        
        if (e is None):
            return None
        elif (e.val == val):
            self.table[key] = e.next
            return val
        else:
            while e.next != None:
                if e.next.val == val:
                    e.next = e.next.next
                    return val
                e = e.next
        return None
        
# MAIN        

tbl_size = 2**16
findsize = tbl_size // 10
t = HashTable(tbl_size)
l = []

start_time = time.time()
for i in xrange(tbl_size):
    r = GenRandStr(10)
    l.append(r)
    t.AddVal(r)
end_time = time.time() - start_time
print "Added %d elements to the table: %0.5f" % (tbl_size, end_time)

start_time = time.time()
for i in xrange(findsize):
    r = random.randint(0, len(l)-1)
    #print i, l[r] == t.FindVal(l[r])
    t.FindVal(l[r])
end_time = time.time() - start_time
print "Searched %d random elements in: %0.5f" % (findsize, end_time)

start_time = time.time()
for i in xrange(findsize):
    r = random.randint(0, len(l)-1)
    t.DelVal(l[r])
    del l[r]
end_time = time.time() - start_time
print "Deleted %d random elements in: %0.5f" % (findsize, end_time)

start_time = time.time()
for i in xrange(tbl_size):
    r = GenRandStr(10)
    l.append(r)
    t.AddVal(r)
end_time = time.time() - start_time
print "Added %d elements to the table: %0.5f" % (tbl_size, end_time)

start_time = time.time()
for i in xrange(findsize):
    r = random.randint(0, len(l)-1)
    t.FindVal(l[r])
end_time = time.time() - start_time
print "Searched %d random elements in: %0.5f" % (findsize, end_time)

start_time = time.time()
for i in xrange(findsize):
    r = random.randint(0, len(l)-1)
    t.DelVal(l[r])
    del l[r]
end_time = time.time() - start_time
print "Deleted %d random elements in: %0.5f" % (findsize, end_time)

    