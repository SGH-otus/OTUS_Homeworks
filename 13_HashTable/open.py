import random
import string
import time
import sys

def GenRandStr(str_len):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(str_len))

class HashTable:
    table = []
    dim = 2
    c1 = 1.0 / 2
    c2 = 1.0 / 2
    tmbstn = "###"
     
    def __init__(self, size):
        self.table = [None] * size
        self.Pearson_Table = range(256)
        random.shuffle(self.Pearson_Table)
    
    def Probe(self, i):
        return int((self.c1 * i) + (self.c2 * i**2))
    
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

        i = 0
        while (self.table[(key + self.Probe(i)) % 2**16] != None) and (self.table[(key + self.Probe(i)) % 2**16] != self.tmbstn):
            i = i + 1

        #print val, key, i
        
        self.table[(key + self.Probe(i)) % 2**16] = val
        return
        
    def FindVal(self, val):
        key = self.HashFunc(val)

        i = 0
        while self.table[(key + self.Probe(i)) % 2**16] != None:
            if self.table[(key + self.Probe(i)) % 2**16] == val:
                return val
            i = i + 1
        return None
     
    def DelVal(self, val):
        key = self.HashFunc(val)

        i = 0
        while self.table[(key + self.Probe(i)) % 2**16] != None:
            if self.table[(key + self.Probe(i)) % 2**16] == val:
                self.table[(key + self.Probe(i)) % 2**16] = self.tmbstn
                return val
            i = i + 1
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
for i in xrange(findsize):
    r = GenRandStr(10)
    l.append(r)
    t.AddVal(r)
end_time = time.time() - start_time
print "Added %d elements to the table: %0.5f" % (findsize, end_time)

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

    