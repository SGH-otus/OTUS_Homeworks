import random
import time
import math
import struct
import sys

def gen_rand_arr(size, minrand, maxrand):
    arr = []
    for i in xrange(size):
        arr.append(random.randint(minrand,maxrand))
    return [arr]
    
def gen_rand_file(tempfilename, minrand, maxrand):
    buf = ""
    f = open(tempfilename, "wb")

    for i in xrange(size):
        r = random.randint(minrand, maxrand)
        buf = buf + struct.pack(">H", r) # packs to unsigned 2byte, [minrand:maxrand] == [0:65535]
        if (i % 2**19) == 0:
            f.write(buf)
            buf = ""

    f.write(buf)
    f.close()      
    
def read_rand_file(tempfilename):   
    buf = open(tempfilename, "rb").read()
    arr = []
    i = 0

    maxrand = struct.unpack(">H", buf[0:2])[0] # "2" because unsigned 2byte
    minrand = maxrand

    while i < len(buf):
        r = struct.unpack(">H", buf[i:i+2])[0] # "2" because unsigned 2byte
        arr.append(r)
        if r > maxrand:
            maxrand = r
        if r < minrand:
            minrand = r
        i = i + 2 # "2" because unsigned 2byte

    size = i / 2 # "2" because unsigned 2byte
    return (arr, size, minrand, maxrand)
    
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

def gen_smooth(max): # genereate 3-smooth numbers not greather then 'max', for Pratt's gaps
    n2 = []
    i = 1
    while (2**i < max):
        n2.append(2**i)
        i = i + 1

    n3 = []
    i = 1
    while (3**i < max):
        n3.append(3**i)
        i = i + 1

    n = [1]

    for i2 in n2:
        for i3 in n3:
            if i2 * i3 < max:
                n.append(i2 * i3)
    return sorted(n + n2 + n3)[::-1]

def ShellSort_Shell(arr, left=None, right=None): # classic Shell, gaps = N / 2**k
    gap = len(arr) / 2
    while gap > 0:
        i = 0
        while (i + gap < len(arr)):
            j = i + gap
            tmp = arr[j]
            while ((j - gap >= 0) and (arr[j - gap] > tmp)):
                arr[j] = arr[j - gap]
                j = j - gap
            i = i + 1
        gap = gap / 2
    return arr

def ShellSort_Hibbard(arr, left=None, right=None): # Shell with Hibbard gaps = (2**k) - 1 (OEIS A168604)
    gap = int(math.log(len(arr), 2)) 
    gap = 2**gap - 1
    while gap > 0:
        i = 0
        while (i + gap < len(arr)):
            j = i + gap
            tmp = arr[j]
            while ((j - gap >= 0) and (arr[j - gap] > tmp)):
                arr[j] = arr[j - gap]
                j = j - gap
            i = i + 1
        gap = gap / 2
    return arr

def ShellSort_Pratt_smooth(arr, left=None, right=None): # Shell with Pratt gaps 3-smooth numbers (OEIS A003586)
    smooth  = gen_smooth(len(arr))
    for gap in smooth:
        i = 0
        while (i + gap < len(arr)):
            j = i + gap
            tmp = arr[j]
            while ((j - gap >= 0) and (arr[j - gap] > tmp)):
                arr[j] = arr[j - gap]
                j = j - gap
            i = i + 1
    return arr

def HeapSort(arr, left=None, right=None): 
    def swap(x, y):
        t = arr[x]
        arr[x] = arr[y]
        arr[y] = t 
    
    def down(size, root):
        L = 2 * root + 1
        R = L + 1
        x = root
        
        if ((L < size) and (arr[L] > arr[x])):
            x = L
        
        if ((R < size) and (arr[R] > arr[x])):
            x = R
        
        if (x == root): 
            return
        
        swap(root, x)
        down(size, x)
    
    for node in range(len(arr) / 2 - 1, -1, -1):
        down(len(arr), node)
    
    for size in range(len(arr) - 1, -1, -1):
        swap(0, size)
        down(size, 0)
    return arr

def QuickSort(arr, left, right): 
    def partition(left, right):
        i = left - 1
        pivot = arr[right]
        for j in range(left, right + 1):
            if arr[j] <= pivot:
                i = i + 1
                t = arr[i]
                arr[i] = arr[j]
                arr[j] = t
        return i

    if left >= right:
        return arr 
    else:
        center = partition(left, right)
        QuickSort(arr, left, center - 1)
        QuickSort(arr, center + 1, right)
        return arr
        
def MergeSort(arr, left, right, part_size, helper_sort_func): 
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
        
    if (right - left <= part_size):
        r = helper_sort_func(arr[left:right + 1], 0, right - left)
        arr[left:right + 1] = r
    else:
        center = left + ((right - left) / 2)
        MergeSort(arr, left, center, part_size, helper_sort_func)
        MergeSort(arr, center + 1, right, part_size, helper_sort_func)
        merge(left, center, right)

# MAIN

size = 10**6 # size of array to sort
minrand = -10000 # minimum integer to generate as array member
maxrand = 10000 # maximum integer to generate as array member
MS_part_size = 256 # MergeSort part size for another sort algo
mix_coeff = 100 # how many elements to mix (1/coeff)

GENERATE_FILE = False
READ_FROM_FILE = False
tempfilename = "tempfile.bin"

if GENERATE_FILE:
    gen_rand_file(tempfilename, 0, 2**16 - 1)
    print "Generated %d numbers [ %d ; %d ], saved in file \"%s\""  % (size, minrand, maxrand, tempfilename)

def get_arr(flag, silent):
    global size, minrand, maxrand
    if flag:
        (arr, size, minrand, maxrand) = read_rand_file(tempfilename)
        get_arr = read_rand_file(tempfilename)
        if not silent:
            print "Read %d elements [ %d ; %d ] from file \"%s\"" % (size, minrand, maxrand, tempfilename)
    else:
        arr = gen_rand_arr(size, minrand, maxrand)[0]
        get_arr = gen_rand_arr(size, minrand, maxrand)
        if not silent:
            print "Generated %d elements [ %d ; %d ]" % (size, minrand, maxrand)
    return arr
    
arr = get_arr(READ_FROM_FILE, False)

print
print "Name \t\t\t\t\t\t Time \t\t Correct"
print "=" * 72

#arr = get_arr(READ_FROM_FILE)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, -1, None)
end_time = time.time() - start_time
print "MergeSort (clean) of of random: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, -1, None)
end_time = time.time() - start_time
print "MergeSort (clean) of sort + mix: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

print
print "Combined MergeSort with part size %d:" % (MS_part_size)
print

# MergeSort + Shell
arr = get_arr(READ_FROM_FILE, True)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, ShellSort_Shell)
end_time = time.time() - start_time
print "MergeSort + ShellSort (S) of random: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, ShellSort_Shell)
end_time = time.time() - start_time
print "MergeSort + ShellSort (S) of sort + mix: \t %0.5f \t %r" % (end_time, arr == sorted(arr))
print

# MergeSort + Shell (Hibbard)
arr = get_arr(READ_FROM_FILE, True)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, ShellSort_Hibbard)
end_time = time.time() - start_time
print "MergeSort + ShellSort (H) of random: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, ShellSort_Hibbard)
end_time = time.time() - start_time
print "MergeSort + ShellSort (H) of sort + mix: \t %0.5f \t %r" % (end_time, arr == sorted(arr))
print

# MergeSort + Shell (Pratt)
arr = get_arr(READ_FROM_FILE, True)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, ShellSort_Pratt_smooth)
end_time = time.time() - start_time
print "MergeSort + ShellSort (P) of random: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, ShellSort_Pratt_smooth)
end_time = time.time() - start_time
print "MergeSort + ShellSort (P) of sort + mix: \t %0.5f \t %r" % (end_time, arr == sorted(arr))
print

# MergeSort + HeapSort
arr = get_arr(READ_FROM_FILE, True)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, HeapSort)
end_time = time.time() - start_time
print "MergeSort + HeapSort of random: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, HeapSort)
end_time = time.time() - start_time
print "MergeSort + HeapSort of sort + mix: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))
print

# MergeSort + QuickSort
arr = get_arr(READ_FROM_FILE, True)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, QuickSort)
end_time = time.time() - start_time
print "MergeSort + QuickSort of random: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, QuickSort)
end_time = time.time() - start_time
print "MergeSort + QuickSort of sort + mix: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

print
print
print
print

size = 10**5
minrand = -10 
maxrand = 10
MS_part_size = 32

arr = gen_rand_arr(size, minrand, maxrand)[0]
print "Generated %d elements [ %d ; %d ] (low-dispersed)" % (size, minrand, maxrand)
print

print "Name \t\t\t\t\t\t Time \t\t Correct"
print "=" * 72

# Clean MergeSort
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, -1, None)
end_time = time.time() - start_time
print "MergeSort (clean) of random: \t\t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, -1, None)
end_time = time.time() - start_time
print "MergeSort (clean) of sort + mix: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

print
print "Combined MergeSort with part size %d:" % (MS_part_size)
print

# MergeSort + Shell
arr = gen_rand_arr(size, minrand, maxrand)[0]
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, ShellSort_Shell)
end_time = time.time() - start_time
print "MergeSort + ShellSort (S) of random: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, ShellSort_Shell)
end_time = time.time() - start_time
print "MergeSort + ShellSort (S) of sort + mix: \t %0.5f \t %r" % (end_time, arr == sorted(arr))
print

# MergeSort + Shell (Hibbard)
arr = gen_rand_arr(size, minrand, maxrand)[0]
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, ShellSort_Hibbard)
end_time = time.time() - start_time
print "MergeSort + ShellSort (H) of random: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, ShellSort_Hibbard)
end_time = time.time() - start_time
print "MergeSort + ShellSort (H) of sort + mix: \t %0.5f \t %r" % (end_time, arr == sorted(arr))
print

# MergeSort + Shell (Pratt)
arr = gen_rand_arr(size, minrand, maxrand)[0]
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, ShellSort_Pratt_smooth)
end_time = time.time() - start_time
print "MergeSort + ShellSort (P) of random: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, ShellSort_Pratt_smooth)
end_time = time.time() - start_time
print "MergeSort + ShellSort (P) of sort + mix: \t %0.5f \t %r" % (end_time, arr == sorted(arr))
print

# MergeSort + HeapSort
arr = gen_rand_arr(size, minrand, maxrand)[0]
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, HeapSort)
end_time = time.time() - start_time
print "MergeSort + HeapSort of random: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, HeapSort)
end_time = time.time() - start_time
print "MergeSort + HeapSort of sort + mix: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))
print

# MergeSort + QuickSort
arr = gen_rand_arr(size, minrand, maxrand)[0]
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, QuickSort)
end_time = time.time() - start_time
print "MergeSort + QuickSort of random: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff)
start_time = time.time()
MergeSort(arr, 0, len(arr) - 1, MS_part_size, QuickSort)
end_time = time.time() - start_time
print "MergeSort + QuickSort of sort + mix: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))
print
