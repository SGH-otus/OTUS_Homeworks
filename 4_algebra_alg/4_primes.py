# -*- coding: utf-8 -*-
import time
import gc

'''
3. Алгоритмы поиска кол-ва простых чисел до N макс. 6 байт
3a. Через перебор делителей.
+1 байт 3b. Несколько оптимизаций перебора делителей, с использованием массива.
+1 байт 3c. Решето Эратосфена со сложностью O(n log log n).
+1 байт 3d. Решето Эратосфена с оптимизацией памяти: битовая матрица, по 32 значения в одном int
+1 байт 3e. Решето Эратосфена со сложностью O(n)
+2 байт Составить сравнительную таблицу времени работы алгоритмов для разных начальных данных.
Написать, какие пункты выполнены и сколько времени ушло на выполнение домашнего задания.

'''

def primes_3a(n):
    r = 0
    for i in range(2, n):
        c = 0
        for j in range(1, n):
            if i % j == 0:
                c = c + 1 
        if c == 2:
            r = r + 1
    return r

def primes_3b(n):
    arr = [2]
    for i in range(3, n):
        flag = False
        for j in arr:
            if i % j == 0:
                flag = True
                break
        if not flag:
            arr.append(i)
    return len(arr)
    
def primes_3c(n):
    arr = []
    c = 0
    for i in range(n):
        arr.append(i)
    
    for i in range(2, len(arr)):
        if arr[i] != 0:
            c = c + 1
            for j in range(i + i, len(arr), arr[i]):
                arr[j] = 0
    return c

def primes_3d(n):
    def getbit(n, i):
        return n >> i & 1

    def setbit(n, i):
        return n & ((1 << i) ^ 0xFFFFFFFF )

    arr = []
    c = 0
    
    for i in range(n // 8 + 1):
        arr.append(0xFFFFFFFF)
        
    for i in range(2, n):
        if getbit(arr[i // 8], i % 8) != 0:
            c = c + 1
            for j in range(i + i, n, i):
                arr[j // 8] = setbit(arr[j // 8], j % 8)
    return c
    
def primes_3e(n):
    lp = [0] * (n + 1)
    pr = []
    
    for i in range(2, n):
        if lp[i] == 0:
            lp[i] = i
            pr.append(i)
        for p in pr:
            if (p > lp[i]) or (p * i > n):
                break
            lp[p * i] = p

    return len(pr)

start_time = time.time()    
r1 = primes_3a(3000)
end_time = time.time() - start_time
print "primes_3a", r1, "%0.5f" % end_time, '\t' 

start_time = time.time()    
r2 = primes_3b(50000)
end_time = time.time() - start_time
print "primes_3b", r2, "%0.5f" % end_time, '\t' 

start_time = time.time()    
r3 = primes_3c(500000)
end_time = time.time() - start_time
print "primes_3c", r3, "%0.5f" % end_time, '\t' 

start_time = time.time()    
r4 = primes_3d(500000)
end_time = time.time() - start_time
print "primes_3d", r4, "%0.5f" % end_time, '\t' 

start_time = time.time()    
r5 = primes_3e(5000000)
end_time = time.time() - start_time
print "primes_3e", r5, "%0.5f" % end_time, '\t' 

gc.collect()

"""
arr = []
start_time = time.time()  
for i in range(500000):
    arr.append(i)
end_time = time.time() - start_time
print "test", "%0.5f" % end_time, '\t' 
"""