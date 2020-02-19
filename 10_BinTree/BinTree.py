import random
import time
import sys
import gc

class Leaf:
    #key = None
    val = None
    cnt = 0
    parent = None
    left = None
    right = None

    def __init__(self, val):
        self.val = val

class BinTree:
    tree_root = None
    
    def AddNode(self, root, node):
        if node.val == root.val:
            root.cnt = root.cnt + 1
            del node
        elif node.val < root.val:
            if root.left:
                self.AddNode(root.left, node)
            else:
                root.left = node
                node.parent = root
        elif node.val > root.val:
            if root.right:
                self.AddNode(root.right, node)
            else:
                root.right = node
                node.parent = root
     
    def AddVal(self, val):
        l = Leaf(val)
        if self.tree_root == None:
            self.tree_root = l
        else:
            self.AddNode(self.tree_root, l)
                
    def FindVal(self, root, val):
        if val == root.val:
            return root

        if val < root.val:
            if root.left:
                return self.FindVal(root.left, val)
            else:
                return None
        else:
            if root.right:
                return self.FindVal(root.right, val)
            else:
                return None
     
    def DelVal(self, val):
        cur_leaf = self.FindVal(self.tree_root, val)
        if cur_leaf:
            if cur_leaf.cnt > 0:
                cur_leaf.cnt = cur_leaf.cnt - 1
                return
            p = cur_leaf.parent
            if p == None:
                l = cur_leaf.left
                r = cur_leaf.right
                if cur_leaf.left:
                    cur_leaf.left.parent = None
                    cur_leaf.AddNode(r)
                    cur_leaf = l
                    return
                if cur_leaf.right:
                    cur_leaf.right.parent = None
                    cur_leaf = r
            else:
                if p.left == cur_leaf:
                    p.left = None
                else:
                    p.right = None
                    
                if cur_leaf.left:
                    self.AddNode(p, cur_leaf.left)
                if cur_leaf.right:
                    self.AddNode(p, cur_leaf.right)
            del cur_leaf

    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print self.val,
        if self.right:
            self.right.PrintTree()

# MAIN        

print "Working with random numbers, recursion limit:", sys.getrecursionlimit()

t = BinTree()
l = []

size = 100000 # size of tree
minrand = -1000000 # minimum integer to generate as tree member
maxrand =  1000000 # maximum integer to generate as tree member
findsize = size // 10

start_time = time.time()
for i in xrange(size):
    r = random.randint(minrand, maxrand)
    l.append(r)
    t.AddVal(r)
end_time = time.time() - start_time
print "Added %d elements to the tree: %0.5f" % (size, end_time)

start_time = time.time()
for i in xrange(findsize):
    r = random.randint(0, len(l)-1)
    t.FindVal(t.tree_root, r)
end_time = time.time() - start_time
print "Searched %d random elements in: %0.5f" % (findsize, end_time)
    
start_time = time.time()
for i in xrange(findsize):
    r = random.randint(0, len(l)-1)
    t.DelVal(l[r])
    del l[r]
end_time = time.time() - start_time
print "Deleted %d random elements in: %0.5f" % (findsize, end_time)

for i in xrange(size):
    r = random.randint(minrand, maxrand)
    l.append(r)
    t.AddVal(r)
    end_time = time.time() - start_time
print "Added %d elements to the tree: %0.5f" % (size, end_time)

start_time = time.time()
for i in xrange(findsize):
    r = random.randint(0, len(l)-1)
    t.FindVal(t.tree_root, r)
end_time = time.time() - start_time
print "Searched %d random elements in: %0.5f" % (findsize, end_time)

start_time = time.time()
for i in xrange(findsize):
    r = random.randint(0, len(l)-1)
    t.DelVal(l[r])
    del l[r]
end_time = time.time() - start_time
print "Deleted %d random elements in: %0.5f" % (findsize, end_time)

t = None
l = []
gc.collect() # just curious how it works =)
    
print
sys.setrecursionlimit(10000) # program crashes with small numbers of this parameter
print "Working with increasing numbers, recursion limit:", sys.getrecursionlimit()
size = 2200
findsize = size // 10

t = BinTree()
l = []

start_time = time.time()
for i in xrange(size):
    r = i
    l.append(r)
    t.AddVal(r)
end_time = time.time() - start_time
print "Added %d elements to the tree: %0.5f" % (size, end_time)

start_time = time.time()
for i in xrange(findsize):
    r = random.randint(0, len(l)-1)
    t.FindVal(t.tree_root, r)
end_time = time.time() - start_time
print "Searched %d random elements in: %0.5f" % (findsize, end_time)
    
start_time = time.time()
for i in xrange(findsize):
    r = random.randint(0, len(l)-1)
    t.DelVal(l[r])
    del l[r]
end_time = time.time() - start_time
print "Deleted %d random elements in: %0.5f" % (findsize, end_time)
    
start_time = time.time()
for i in xrange(size,size*2):
    r = i
    l.append(r)
    t.AddVal(r)
end_time = time.time() - start_time
print "Added %d elements to the tree: %0.5f" % (size, end_time)

start_time = time.time()
for i in xrange(findsize):
    r = random.randint(0, len(l)-1)
    t.FindVal(t.tree_root, r)
end_time = time.time() - start_time
print "Searched %d random elements in: %0.5f" % (findsize, end_time)
    
start_time = time.time()
for i in xrange(findsize):
    r = random.randint(0, len(l)-1)
    t.DelVal(l[r])
    del l[r]
end_time = time.time() - start_time
print "Deleted %d random elements in: %0.5f" % (findsize, end_time)
    
    