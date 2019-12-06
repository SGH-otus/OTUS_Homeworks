import random
import time
import math

size = 40000 # size of array to sort
minrand = -100000 # minimum integer to generate as array member
maxrand = 100000 # maximum integer to generate as array member

def gen_rand_arr():
    arr = []
    for i in range(size):
        arr.append(random.randint(minrand,maxrand))
    return arr
    
def mixelems(cnt): # mix 'cnt' random elements in the array
    global arr
    for i in range(cnt):
        pos = random.randint(0, size - 1)
        t = arr[pos]
        del arr[pos]
        pos = random.randint(0, size - 1)
        arr.insert(pos, t)    

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
            if i2 * i3<size:
                n.append(i2 * i3)
    return sorted(n + n2 + n3)[::-1]

def ShellSort_Shell(): # classic Shell, gaps = N / 2**k
    global arr # sort orignal array, instead of copy, how it is passed to function
    gap = size / 2
    while gap > 0:
        i = 0
        while (i + gap < size):
            j = i + gap
            tmp = arr[j]
            while ((j - gap >= 0) and (arr[j - gap] > tmp)):
                arr[j] = arr[j - gap]
                j = j - gap
            i = i + 1
        gap = gap / 2

def ShellSort_Hibbard(): # Shell with Hibbard gaps = (2**k) - 1 (OEIS A168604)
    global arr
    gap = int(math.log(size,2)) 
    gap = 2**gap - 1
    while gap > 0:
        i = 0
        while (i + gap < size):
            j = i + gap
            tmp = arr[j]
            while ((j - gap >= 0) and (arr[j - gap] > tmp)):
                arr[j] = arr[j - gap]
                j = j - gap
            i = i + 1
        gap = gap / 2

def ShellSort_Pratt_smooth(): # Shell with Pratt gaps 3-smooth numbers (OEIS A003586)
    global arr
    smooth  = gen_smooth(size)
    for gap in smooth:
        i = 0
        while (i + gap < size):
            j = i + gap
            tmp = arr[j]
            while ((j - gap >= 0) and (arr[j - gap] > tmp)):
                arr[j] = arr[j - gap]
                j = j - gap
            i = i + 1

print "%d elements [ %d ; %d ]" % (size, minrand, maxrand)

# PURE SHELL
arr = gen_rand_arr()

print
start_time = time.time()
ShellSort_Shell()
end_time = time.time() - start_time
print "Sorted correctly: ", arr == sorted(arr)
print "ShellSort (Shell) of random: %0.5f" % (end_time)

mixelems(size / 10)
start_time = time.time()
ShellSort_Shell()
end_time = time.time() - start_time
print "ShellSort (Shell) of 10 %% random: %0.5f" % (end_time)

mixelems(5)
start_time = time.time()
ShellSort_Shell()
end_time = time.time() - start_time
print "ShellSort (Shell) of 5 random: %0.5f" % (end_time)
    
# HIBBARD
print
arr = gen_rand_arr()

start_time = time.time()
ShellSort_Hibbard()
end_time = time.time() - start_time
print "Sorted correctly: ", arr == sorted(arr)
print "ShellSort (Hibbard) of random: %0.5f" % (end_time), arr == sorted(arr)

mixelems(size / 10)
start_time = time.time()
ShellSort_Hibbard()
end_time = time.time() - start_time
print "ShellSort (Hibbard) of 10 %% random: %0.5f" % (end_time)

mixelems(5)
start_time = time.time()
ShellSort_Hibbard()
end_time = time.time() - start_time
print "ShellSort (Hibbard) of 5 random: %0.5f" % (end_time)
    
# PRATT SMOOTH
print
arr = gen_rand_arr()

start_time = time.time()
ShellSort_Pratt_smooth()
end_time = time.time() - start_time
print "Sorted correctly: ", arr == sorted(arr)
print "ShellSort (Pratt Smooth) of random: %0.5f" % (end_time), arr == sorted(arr)

mixelems(size / 10)
start_time = time.time()
ShellSort_Pratt_smooth()
end_time = time.time() - start_time
print "ShellSort (Pratt Smooth) of 10 %% random: %0.5f" % (end_time)

mixelems(5)
start_time = time.time()
ShellSort_Pratt_smooth()
end_time = time.time() - start_time
print "ShellSort (Pratt Smooth) of 5 random: %0.5f" % (end_time)