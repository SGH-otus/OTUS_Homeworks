import random
import time
import math
import struct
import sys

def gen_rand_arr(size, minrand, maxrand):
    arr = []
    for i in xrange(size):
        arr.append(random.randint(minrand,maxrand))
    return arr
    
def mixelems(arr, cnt): # mix 'cnt' random elements in the array
    sys.stdout.write("Mixing... ")
    for i in xrange(cnt):
        pos1 = random.randint(0, len(arr) - 1)
        pos2 = random.randint(0, len(arr) - 1)
        t = arr[pos1]
        arr[pos2] = arr[pos1]
        arr[pos1] = t
    sys.stdout.write("\r             ")
    sys.stdout.write("\r")    
    sys.stdout.flush()

def MergeSort(arr, left, right): 
    
    def merge(left, center, right):
        arr3 = []
        i = left
        j = center + 1
            
        while (i <= center) and (j <= right):
            if (arr[i] < arr[j]):
                arr3.append(arr[i])
                i = i + 1
            else:
                arr3.append(arr[j])
                j = j + 1
        
        arr3.extend(arr[i:center + 1])
        arr3.extend(arr[j:right + 1])
        
        arr[left:right + 1] = arr3[:]
        
        return
    
    if left >= right:
        return
        
    center = left + ((right - left) / 2)
    MergeSort(arr, left, center)
    MergeSort(arr, center + 1, right)
    merge(left, center, right)

# MAIN

size = 10**6 # size of array to sort
minrand = 0 # minimum integer to generate as array member
maxrand = 65535 # maximum integer to generate as array member
mix_coeff = 10000 # how mane elements to mix in sorted array

GENERATE_FILE = False
READ_FROM_FILE = False
tempfilename = "tempfile.bin"

if GENERATE_FILE:
    buf = ""
    f = open(tempfilename, "wb")

    for i in xrange(size):
        r = random.randint(minrand, maxrand)
        buf = buf + struct.pack(">H", r)
        if (i % 2**19) == 0:
            f.write(buf)
            buf = ""

    f.write(buf)
    f.close()  
    print "Generated %d numbers [ %d ; %d ], saved in file \"%s\""  % (size, minrand, maxrand, tempfilename)

if READ_FROM_FILE:
    buf = open(tempfilename, "rb").read()
    arr = []
    i = 0

    maxrand = struct.unpack(">H", buf[0:2])[0]
    minrand = maxrand

    while i < len(buf):
        r = struct.unpack(">H", buf[i:i+2])[0]
        arr.append(r)
        if r > maxrand:
            maxrand = r
        if r < minrand:
            minrand = r
        i = i + 2

    size = i / 2

    print "Read %d elements [ %d ; %d ] from file \"%s\"" % (size, minrand, maxrand, tempfilename)
else:
    arr = gen_rand_arr(size, minrand, maxrand)
    print "Generated %d elements [ %d ; %d ]" % (size, minrand, maxrand)

print

start_time = time.time()
MergeSort(arr, 0, len(arr) - 1)
end_time = time.time() - start_time
print "Sorted correctly: ", arr == sorted(arr)
print "MergeSort of random: %0.5f" % (end_time)
mixelems(arr, mix_coeff)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1)
end_time = time.time() - start_time
print "MergeSort of sort + mix:: %0.5f" % (end_time)
