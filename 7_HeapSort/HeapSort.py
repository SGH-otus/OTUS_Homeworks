import random
import time
import math
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

def HeapSort(arr): 
    
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
# MAIN

size = 200000 # size of array to sort
minrand = -100000 # minimum integer to generate as array member
maxrand = 100000 # maximum integer to generate as array member
mix_coeff1 = 10 # how many elements to mix
mix_coeff2 = 20 # how many elements to mix

arr = gen_rand_arr(size, minrand, maxrand)
print "Generated %d elements [ %d ; %d ]" % (size, minrand, maxrand)

start_time = time.time()
HeapSort(arr)
end_time = time.time() - start_time
print "Sorted correctly: ", arr == sorted(arr)
print "HeapSort of random: %0.5f" % (end_time)

mixelems(arr, size / mix_coeff1)
start_time = time.time()
HeapSort(arr)
end_time = time.time() - start_time
print "HeapSort of %0.2f %% random: %0.5f" % ((100.0) / mix_coeff1, end_time)

mixelems(arr, size / mix_coeff2)
start_time = time.time()
HeapSort(arr)
end_time = time.time() - start_time
print "HeapSort of %0.2f %% random: %0.5f" % ((100.0) / mix_coeff2, end_time)

print
size = 100000 # empirical value, there is possibility to exceed recursion limit
minrand = -10 
maxrand = 10
arr = gen_rand_arr(size, minrand, maxrand)
start_time = time.time()
HeapSort(arr)
end_time = time.time() - start_time
print "%d elements [ %d ; %d ] (low-dispersed)" % (size, minrand, maxrand)
print "Sorted correctly: ", arr == sorted(arr)
print "HeapSort of random: %0.5f" % (end_time)

mixelems(arr, size / mix_coeff1)
start_time = time.time()
HeapSort(arr)
end_time = time.time() - start_time
print "HeapSort of %0.2f %% random: %0.5f" % ((100.0) / mix_coeff1, end_time)

mixelems(arr, size / mix_coeff2)
start_time = time.time()
HeapSort(arr)
end_time = time.time() - start_time
print "HeapSort of %0.2f random: %0.5f" % ((100.0) / mix_coeff2, end_time)
