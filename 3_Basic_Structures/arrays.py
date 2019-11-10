# -*- coding: utf8 -*-

'''
1 задание. Динамические массивы.
Написать метод добавления и удаления элементов:
void add(T item, int index);
T remove(int index); // возвращает удаляемый элемент
по индексу во все варианты динамических массивов:
SingleArray, VectorArray, FactorArray, MatrixArray *.
+1 балл.

2 задание. Таблица сравнения производительности.
Сравнить время выполнения разных операций
для разных массивов с разным порядком значений.
* сделать обёртку над ArrayList() и тоже сравнить.
Составить таблицу и приложить её скриншот.
Сделать выводы и сформулировать их в нескольких предложениях.
+1 балл.

'''
import time

class SingleArray:
    arr = []
    arr_size = 0

    def __init__(self):
        self.arr = [0]
        self.arr_size = 0
        return None

    def get(self, index):
        return self.arr[index]
    
    def add(self, item):
        self.arr = self.arr[:] + [0]
        self.arr[self.arr_size] = item
        self.arr_size = self.arr_size + 1
        return 0
    
    def insert(self, item, index):
        self.arr = self.arr[:] + []
        self.arr = self.arr[:index] + [item] + self.arr[index:]
        self.arr_size = self.arr_size + 1
        return 0
    
    def remove(self, index):
        e = self.arr[index]
        self.arr = self.arr[:index] + self.arr[index + 1:]
        self.arr_size = self.arr_size - 1
        return e
    
    def size(self):
        return self.arr_size
        
class VectorArray:
    arr = [0]
    vector = 10
    arr_size = 0
    
    def __init__(self, vector):
        self.vector = vector
        self.arr = [0] * vector
        self.arr_size = 0
        return None

    def get(self, index):
        return self.arr[index]

    def add(self, item):
        if self.arr_size == len(self.arr):
           self.arr = self.arr + ([0] * self.vector)
        
        self.arr[self.arr_size] = item
        self.arr_size = self.arr_size + 1
        return 0

    def insert(self, item, index):
        if self.arr_size == len(self.arr):
           self.arr = self.arr + ([0] * self.vector)
        
        self.arr = self.arr[:index] + [item] + self.arr[index:]
        self.arr_size = self.arr_size + 1
        return 0
    
    def remove(self, index):
        e = self.arr[index]
        self.arr = self.arr[:index] + self.arr[index + 1:]
        self.arr_size = self.arr_size - 1 
        return e
    
    def size(self):
        return self.arr_size

class FactorArray:
    arr = [0]
    factor = 10
    arr_size = 0
    
    def __init__(self, factor, initlen):
        self.factor = factor
        self.arr = [0] * initlen
        self.arr_size = 0
        return None

    def get(self, index):
        return self.arr[index]

    def add(self, item):
        if self.arr_size == len(self.arr):
            if ( len(self.arr) * self.factor // 100) ==0 :
                self.arr = self.arr + ([0])
            else:
                self.arr = self.arr + ([0] * ( len(self.arr) * self.factor // 100))
        
        self.arr[self.arr_size] = item
        self.arr_size = self.arr_size + 1
        return 0

    def insert(self, item, index):
        if self.arr_size == len(self.arr):
            if ( len(self.arr) * self.factor // 100) ==0 :
                self.arr = self.arr + ([0])
            else:
                self.arr = self.arr + ([0] * ( len(self.arr) * self.factor // 100))
           
        self.arr = self.arr[:index] + [item] + self.arr[index:]
        self.arr_size = self.arr_size + 1
        return 0
    
    def remove(self, index):
        e = self.arr[index]
        self.arr = self.arr[:index] + self.arr[index + 1:]
        self.arr_size = self.arr_size - 1 
        return e
    
    def size(self):
        return self.arr_size

class MatrixArray:
    arr = []
    vector = 10
    arr_size = 0
    
    def __init__(self, vector):
        self.vector = vector
        self.arr = SingleArray()
        self.arr.add(VectorArray(self.vector))
        self.arr_size = 0
        return None

    def get(self, index):
        return self.arr.get(index // self.vector).get(index % self.vector)

    def add(self, item):
        if self.arr_size == self.arr.size() * self.vector:
            self.arr.add(VectorArray(self.vector))
            
        self.arr.get(self.size() // self.vector).add(item)
        self.arr_size = self.arr_size + 1
        return 0

    def insert(self, item, index):
        if ((index // self.vector) == ((self.arr_size-1) // self.vector)):
            self.arr.get(index // self.vector).insert(item, index % self.vector)
            return 0

        e1 = self.arr.get(index // self.vector).remove(self.arr.get(index // self.vector).size() - 1)
        self.arr.get(index // self.vector).insert(item, index % self.vector)
        
        for i in range(index // self.vector + 1, self.arr_size // self.vector):
            #print self.arr.get(i).arr
            e2 = self.arr.get(i).remove(self.arr.get(i).size())
            self.arr.get(i).insert(e1, 0)
            e1 = self.arr.get(i).get(self.arr.get(i).size())
            #self.arr.get(i).insert(e2, self.arr.get(i).size())
            #print self.arr.get(i).arr
        
        if self.arr_size == self.arr.size() * self.vector:
            self.arr.add(VectorArray(self.vector))

        self.arr_size = self.arr_size + 1
        return 0
    
    def remove(self, index):
        e = self.arr.get(index // self.vector).remove(index % self.vector)
        if ((index // self.vector) == ((self.arr_size-1) // self.vector)):
            return e
       
        self.arr.get(index // self.vector).add(self.arr.get(index // self.vector + 1).get(0))

        for i in range(index // self.vector + 1, self.arr_size // self.vector - 1):
            self.arr.get(i).remove(0)
            self.arr.get(i).add(self.arr.get(i + 1).get(0))

        self.arr_size = self.arr_size - 1 
        return e
    
    def size(self):
        return self.arr_size

def test_array(a, total):
    start_time = time.time()
    for i in range(0, total):
        a.add(i)
    end_time = time.time() - start_time

    #a.remove(997)
    #a.insert(1111, 997)

    print "%s: %d at %.2fs" % (a.__class__.__name__, total,  end_time)

sa = SingleArray()
test_array(sa, 10000)
va = VectorArray(100)
test_array(va, 100000)
fa = FactorArray(50, 100)
test_array(fa, 100000)
ma = MatrixArray(100)
test_array(ma, 10000)

#for i in range(0, ma.size()):
#    print ma.get(i)

start_time = time.time()
a = []
for i in range(100000):
    a.append(i)

end_time = time.time() - start_time
print "list:        100000 %.2fs" % (end_time)
