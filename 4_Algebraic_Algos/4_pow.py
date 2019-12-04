# -*- coding: utf-8 -*-
import time

'''
2. Алгоритм возведения в степень макс. 4 байта
2а. Итеративный (n умножений)
+1 байт 2b. Через степень двойки с домножением
+1 байт 2c. Через двоичное разложение показателя степени.
+2 байт Составить сравнительную таблицу времени работы алгоритмов для разных начальных данных.
Написать, какие пункты выполнены и сколько времени ушло на выполнение домашнего задания.

'''

def pow_2a(a, b):
    r = 1
    for i in range(b):
        r = r * a
    return r

def pow_2b(a, b):
    r = a
    i = 1
    while i * 2 <= b:
        r = r * r
        i = i * 2
    for j in range(b - i):
        r = r * a
    return r

def pow_2c(a, b):
    r = 1
    t = a
    while b > 0:
        if (b % 2) == 1:
            r = r * t
        t = t * t
        b = b >> 1
    return r

a = 2
b = 129 * 1024

start_time = time.time()    
r1 = pow_2a(a, b)
end_time = time.time() - start_time
print 'pow_2a', end_time

start_time = time.time()    
r2 = pow_2b(a, b)
end_time = time.time() - start_time
print 'pow_2b', end_time

start_time = time.time()    
r3 = pow_2c(a, b)
end_time = time.time() - start_time
print 'pow_2c', end_time 

print r1 == r2 == r3