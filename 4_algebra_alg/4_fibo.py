# -*- coding: utf-8 -*-
import time

'''
4. Алгоритм поиска чисел Фибоначчи макс. 6 байта
4a. Через рекурсию
+1 байт 4b. Через итерацию
+1 байт 4c. По формуле золотого сечения
+2 байт 4d. Через умножение матриц
+2 байт Составить сравнительную таблицу времени работы алгоритмов для разных начальных данных.
Написать, какие пункты выполнены и сколько времени ушло на выполнение домашнего задания.
'''

def fib_4a(a):
    if (a == 1) or (a == 2):
        return 1
    else:
        return fib_4a(a - 2) + fib_4a(a - 1)    

def fib_4b(a):
    n1 = 1
    n2 = 1
    for i in range(a, 3, -1):
        n2 = n1 + n2
        n1 = n2 - n1
    return n1 + n2 

def fib_4c(a):
    f = (1.0 + (5 ** 0.5)) / 2.0
    f = ((f ** a) / (5 ** 0.5)) + 0.5
    return int((f))

def fib_4d(a):
    class fib_matrix:
        matr = [[1, 1], [1, 0]]
        
        def mul(self, m):
            e00 = self.matr[0][0] * m[0][0] + self.matr[0][1] * m[1][0]
            e01 = self.matr[0][0] * m[0][1] + self.matr[0][1] * m[1][1]
            e10 = self.matr[1][0] * m[0][0] + self.matr[1][1] * m[1][0]
            e11 = self.matr[1][0] * m[0][1] + self.matr[1][1] * m[1][1]
            self.matr = [[e00, e01],[e10, e11]]
            return

        def square(self):
            e00 = self.matr[0][0] * self.matr[0][0] + self.matr[0][1] * self.matr[1][0]
            e01 = self.matr[0][0] * self.matr[0][1] + self.matr[0][1] * self.matr[1][1]
            e10 = self.matr[1][0] * self.matr[0][0] + self.matr[1][1] * self.matr[1][0]
            e11 = self.matr[1][0] * self.matr[0][1] + self.matr[1][1] * self.matr[1][1]
            self.matr = [[e00, e01],[e10, e11]]
            return
            
    r = fib_matrix()
    t = fib_matrix()
    
    a = a - 2
    
    while a > 0:
        if (a % 2) == 1:
            r.mul(t.matr)
        t.square()
        a = a >> 1

    return r.matr[0][0]

print 'Fn \trecursive \titerations \tEqual?'

for a in range(30, 35):
    print "%s:" % a, '\t',
    
    start_time = time.time()    
    r1 = fib_4a(a)
    end_time = time.time() - start_time
    print "%0.5f" % end_time, '\t',
    
    start_time = time.time()    
    r2 = fib_4b(a)
    end_time = time.time() - start_time
    print "%0.5f" % end_time, '\t', r1 == r2

print

print 'Fn \titerations \tformula \tEqual?'
for a in range(65, 75):
    print "%s:" % a, '\t',
   
    start_time = time.time()    
    r2 = fib_4b(a)
    end_time = time.time() - start_time
    print "%0.5f" % end_time, '\t',

    start_time = time.time()    
    r3 = fib_4c(a)
    end_time = time.time() - start_time
    print "%0.5f" % end_time, '\t', r3 == r2

print

print 'Fn \t\titerations \tmatrix \t\tEqual?'
for a in range(200000, 200005):
    print "%s:" % a, '\t',
    
    start_time = time.time()    
    r2 = fib_4b(a)
    end_time = time.time() - start_time
    print "%0.5f" % end_time, '\t',

    start_time = time.time()    
    r4 = fib_4d(a)
    end_time = time.time() - start_time
    print "%0.5f" % end_time, '\t', r2 == r4



