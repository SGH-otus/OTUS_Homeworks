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

def ShellSort_Shell(arr): # classic Shell, gaps = N / 2**k
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

def ShellSort_Hibbard(arr): # Shell with Hibbard gaps = (2**k) - 1 (OEIS A168604)
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

def ShellSort_Pratt_smooth(arr): # Shell with Pratt gaps 3-smooth numbers (OEIS A003586)
    smooth = gen_smooth(len(arr))
    for gap in smooth:
        i = 0
        while (i + gap < len(arr)):
            j = i + gap
            tmp = arr[j]
            while ((j - gap >= 0) and (arr[j - gap] > tmp)):
                arr[j] = arr[j - gap]
                j = j - gap
            i = i + 1

# MAIN

size = 40000 # size of array to sort
minrand = -100000 # minimum integer to generate as array member
maxrand = 100000 # maximum integer to generate as array member
mix_coeff1 = 10 # how many elements to mix
mix_coeff2 = 5 # how many elements to mix

arr = gen_rand_arr(size, minrand, maxrand)
print "Generated %d elements [ %d ; %d ]" % (size, minrand, maxrand)
print
print "Name \t\t\t\t\t Time \t\t Correct"
print "=" * 64

# PURE SHELL
start_time = time.time()
ShellSort_Shell(arr)
end_time = time.time() - start_time
print "ShellSort (Shell) of random: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff1)
start_time = time.time()
ShellSort_Shell(arr)
end_time = time.time() - start_time
print "ShellSort (Shell) of %0.2f %% random: \t %0.5f \t %r" % ((100.0) / mix_coeff1, end_time, arr == sorted(arr))

mixelems(arr, 5)
start_time = time.time()
ShellSort_Shell(arr)
end_time = time.time() - start_time
print "ShellSort (Shell) of %d random: \t\t %0.5f \t %r" % (mix_coeff2, end_time, arr == sorted(arr))
    
# HIBBARD
print
arr = gen_rand_arr(size, minrand, maxrand)

start_time = time.time()
ShellSort_Hibbard(arr)
end_time = time.time() - start_time
print "ShellSort (Hibbard) of random: \t\t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff1)
start_time = time.time()
ShellSort_Hibbard(arr)
end_time = time.time() - start_time
print "ShellSort (Shell) of %0.2f %% random: \t %0.5f \t %r" % ((100.0) / mix_coeff1, end_time, arr == sorted(arr))

mixelems(arr, 5)
start_time = time.time()
ShellSort_Hibbard(arr)
end_time = time.time() - start_time
print "ShellSort (Shell) of %d random: \t\t %0.5f \t %r" % (mix_coeff2, end_time, arr == sorted(arr))
    
# PRATT SMOOTH
print
arr = gen_rand_arr(size, minrand, maxrand)

start_time = time.time()
ShellSort_Pratt_smooth(arr)
end_time = time.time() - start_time
print "ShellSort (Pratt Smooth) of random: \t %0.5f \t %r" % (end_time, arr == sorted(arr))

mixelems(arr, size / mix_coeff1)
start_time = time.time()
ShellSort_Pratt_smooth(arr)
end_time = time.time() - start_time
print "ShellSort (Shell) of %0.2f %% random: \t %0.5f \t %r" % ((100.0) / mix_coeff1, end_time, arr == sorted(arr))

mixelems(arr, 5)
start_time = time.time()
ShellSort_Pratt_smooth(arr)
end_time = time.time() - start_time
print "ShellSort (Shell) of %d random: \t\t %0.5f \t %r" % (mix_coeff2, end_time, arr == sorted(arr))