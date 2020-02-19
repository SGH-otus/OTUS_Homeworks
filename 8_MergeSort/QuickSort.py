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
        return
        
    center = partition(left, right)
    QuickSort(arr, left, center - 1)
    QuickSort(arr, center + 1, right)

# MAIN

size = 10**6 # size of array to sort
minrand = -100000 # minimum integer to generate as array member
maxrand = 100000 # maximum integer to generate as array member
mix_coeff1 = 10 # how many elements to mix
mix_coeff2 = 20 # how many elements to mix

arr = gen_rand_arr(size, minrand, maxrand)
print "Generated %d elements [ %d ; %d ]" % (size, minrand, maxrand)

start_time = time.time()
QuickSort(arr, 0, len(arr) - 1)
end_time = time.time() - start_time
print "Sorted correctly: ", arr == sorted(arr)
print "QuickSort of random: %0.5f" % (end_time)

mixelems(arr, size / mix_coeff1)
start_time = time.time()
QuickSort(arr, 0, len(arr) - 1)
end_time = time.time() - start_time
print "QuickSort of %0.2f %% random: %0.5f" % ((100.0) / mix_coeff1, end_time)

mixelems(arr, size / mix_coeff2)
start_time = time.time()
QuickSort(arr, 0, len(arr) - 1)
end_time = time.time() - start_time
print "QuickSort of %0.2f %% random: %0.5f" % ((100.0) / mix_coeff2, end_time)

print
size = 18000 # empirical value, there is possibility to exceed recursion limit
minrand = -10 
maxrand = 10

arr = gen_rand_arr(size, minrand, maxrand)
print "Generated %d elements [ %d ; %d ] (low-dispersed)" % (size, minrand, maxrand)

start_time = time.time()
QuickSort(arr, 0, len(arr) - 1)
end_time = time.time() - start_time
print "Sorted correctly: ", arr == sorted(arr)
print "QuickSort of random: %0.5f" % (end_time)

mixelems(arr, size / mix_coeff1)
start_time = time.time()
QuickSort(arr, 0, len(arr) - 1)
end_time = time.time() - start_time
print "QuickSort of %0.2f %% random: %0.5f" % ((100.0) / mix_coeff1, end_time)

mixelems(arr, size / mix_coeff2)
start_time = time.time()
QuickSort(arr, 0, len(arr) - 1)
end_time = time.time() - start_time
print "QuickSort of %0.2f %% random: %0.5f" % ((100.0) / mix_coeff2, end_time)
