# -*- coding: utf-8 -*-
import time

'''
1. Алгоритм Евклида поиска НОД макс. 4 байта
1a. Через вычитание
+1 байт 1b. Через остаток
+1 байт 1c. Через битовые операции
+2 байт Составить сравнительную таблицу времени работы алгоритмов для разных начальных данных.
Написать, какие пункты выполнены и сколько времени ушло на выполнение домашнего задания.
'''

def nod_1a(a, b):
    while (a !=0 ) and (b != 0):
        if a >= b:
            a = a - b
        else:
            b = b - a
    return abs(a - b)

def nod_1b(a, b):
    while (a !=0 ) and (b != 0):
        if a >= b:
            a = a % b
        else:
            b = b % a
    return abs(a - b)

def nod_1c_naive(a, b):
    nod = 1
    while (a != 0) and (b != 0):
        if ((a % 2) + (b % 2)) == 0:
            nod = nod * 2
            a = a / 2
            b = b / 2 
     
        if ((a % 2) + (b % 2)) == 1:
            if a % 2 == 0:
                a = a / 2
            else:
                b = b / 2
                
        if ((a % 2) + (b % 2)) == 2:
            if b >= a:
                b = (b - a) / 2
            else:
                a = (a - b) / 2
                
    return nod * abs(a - b)
    
def nod_1c_optim(a, b):
    shift = 0
    
    while (((a | b) & 1) == 0):
        shift = shift + 1
        a = a >> 1
        b = b >> 1
 
    while ((a & 1) == 0):
        a = a >> 1
 
    while (b != 0):
        while ((b & 1) == 0):
            b = b >> 1

        if (a > b):
            t = a
            a = b
            b = t
       
        b = b - a
    return a << shift

a = 108888694504
b = 265252859812

start_time = time.time()    
r = nod_1a(a, b)
end_time = time.time() - start_time
print 'nod_1a', r, end_time 

a = 10888869450418352160768000001 ** 251
b = 265252859812191058636308479999999 ** 251

start_time = time.time()    
r = nod_1b(a, b)
end_time = time.time() - start_time
print 'nod_1b', r, end_time 

start_time = time.time()    
r = nod_1c_naive(a, b)
end_time = time.time() - start_time
print 'nod_1c_naive', r, end_time 

start_time = time.time()    
r = nod_1c_optim(a, b)
end_time = time.time() - start_time
print 'nod_1c_optim', r, end_time 
