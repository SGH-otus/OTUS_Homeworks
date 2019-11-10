# -*- coding: utf8 -*-

'''
3 задание. Приоритетная очередь (на выбор).
Написать реализацию PriorityQueue - очередь с приоритетом.
Варианты реализации - список списков, массив списков
Методы к реализации:
enqueue(int priority, T item) - поместить элемент в очередь
T dequeue() - выбрать элемент из очереди

'''
import time

class record:
    priority = 0
    data = ''
    
    def __init__(self, priority = 0, data = ''):
        self.priority = priority
        self.data = data
        return None    

class Node:
    val = record
    next = None
    
    def __init__(self, priority, data, next=None):
        self.val = record()
        self.val.priority = priority
        self.val.data = data
        self.next = next
        return None 
 
    def get_next(self):
        return self.next

    def set_next(self, next):
        self.next = next
        return None
    
    def get_val(self):
        return self.val
        
    def set_val(self, priority, data):
        self.val.priority = priority
        self.val.data = data
        return None
                
    def is_last(self):
        return self.next == None

class LinkedList:
    head = None
    
    def __init__(self):
        self.head = None
        return None 

    def add(self, priority, data):
        n = Node(priority, data)
        
        if self.head == None:
            self.head = n
            return None
        
        p = self.head
        while not p.is_last():
            p = p.get_next()
        p.set_next(n)
            
        return None

    def pop_head(self):
        if (self.head == None):
            return None
            
        v = self.head.get_val()
        self.head = self.head.get_next()
        
        return [v.priority, v.data]

    def get_priority(self):
        if (self.head == None):
            return None
        
        return self.head.get_val().priority
        
    def is_empty(self):
        return self.head == None


class FactorArray:
    arr = []
    factor = 10
    arr_size = 0
    
    def __init__(self, factor = 10, initlen = 1):
        self.factor = factor
        self.arr = [LinkedList()] * initlen
        self.arr_size = 0
        return None

    def get(self, index):
        return self.arr[index]

    def add(self, item):
        if self.arr_size == len(self.arr):
            if ( len(self.arr) * self.factor // 100) == 0:
                self.arr = self.arr + ([LinkedList])
            else:
                self.arr = self.arr + ([LinkedList] * ( len(self.arr) * self.factor // 100))
        
        self.arr[self.arr_size] = item
        self.arr_size = self.arr_size + 1
        return 0

    def insert(self, item, index):
        if self.arr_size == len(self.arr):
            if ( len(self.arr) * self.factor // 100) ==0 :
                self.arr = self.arr + ([LinkedList])
            else:
                self.arr = self.arr + ([LinkedList] * ( len(self.arr) * self.factor // 100))
           
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

class PriorityQueue:
    pr_queue = []
    
    def __init__(self):
        self.pr_queue = FactorArray()
        return None 

    def enqueue(self, priority, data):
        for i in range(0, self.pr_queue.size()):
            if priority == self.pr_queue.get(i).get_priority():
                self.pr_queue.get(i).add(priority, data)
                return None

            if priority < self.pr_queue.get(i).get_priority():
                ll = LinkedList()
                ll.add(priority, data)
                self.pr_queue.insert(ll, i)
                return None

        ll = LinkedList()
        ll.add(priority, data)
        self.pr_queue.add(ll)
        return None
        
    def dequeue(self):
        v = None
        
        for i in range(self.pr_queue.size() - 1, -1, -1):
            if self.pr_queue.get(i).is_empty():
                self.pr_queue.remove(i)
            else:    
                v = self.pr_queue.get(i).pop_head()
                return v
        
        return v

pq = PriorityQueue()

pq.enqueue(5, 'buy food 1')
pq.enqueue(1, 'cook food 1')
pq.enqueue(2, 'deliver food 1')
pq.enqueue(5, 'buy food 2')
pq.enqueue(1, 'cook food 2')
pq.enqueue(2, 'deliver food 2')

print pq.dequeue()
print pq.dequeue()

print pq.dequeue()
print pq.dequeue()

print pq.dequeue()
print pq.dequeue()

print pq.dequeue()
print pq.dequeue()

pq.enqueue(5, 'buy food 1')
pq.enqueue(1, 'cook food 1')
pq.enqueue(2, 'deliver food 1')
pq.enqueue(5, 'buy food 2')
pq.enqueue(1, 'cook food 2')
pq.enqueue(2, 'deliver food 2')

print pq.dequeue()
print pq.dequeue()

print pq.dequeue()
print pq.dequeue()

print pq.dequeue()
print pq.dequeue()

print pq.dequeue()
print pq.dequeue()

