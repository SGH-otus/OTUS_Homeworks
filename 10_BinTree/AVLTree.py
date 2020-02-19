import random
import time
import sys
import gc

class Leaf:
    height = 1
    val = None
    cnt = 0
    parent = None
    left = None
    right = None
    
    def __init__(self, val):
        self.val = val
    
class AVL_Tree:
    tree_root = None
    BigLeftRotation = None
    BigRightRotation = None

    def __init__(self, val, isFast = False):
        if isFast:
            self.BigLeftRotation = self.BigLeftRotation_fast
            self.BigRightRotation = self.BigRightRotation_fast
        else:
            self.BigLeftRotation = self.BigLeftRotation_slow
            self.BigRightRotation = self.BigRightRotation_slow
        
    def GetHeight(self, node):
        if not (node is None):
            return node.height
        return 0

    def FixHeight(self, node):
        hl = self.GetHeight(node.left)
        hr = self.GetHeight(node.right)
        node.height = max([hl, hr]) + 1
    
    def GetBalance(self, node):
        return self.GetHeight(node.left) - self.GetHeight(node.right)
    
    def AddNode(self, root, node):
        if node.val == root.val:
            root.cnt = root.cnt + 1
            del node
            return root
        elif node.val < root.val:
            if root.left is not None:
                self.AddNode(root.left, node)
            else:
                root.left = node
                node.parent = root
        elif node.val > root.val:
            if root.right is not None:
                self.AddNode(root.right, node)
            else:
                root.right = node
                node.parent = root
        root = self.Rebalance(root)
        return node
 
    def AddVal(self, val):
        l = Leaf(val)
        if self.tree_root is None:
            self.tree_root = l
        else:
            self.AddNode(self.tree_root, l)
        return l
                
    def FindVal(self, root, val):
        if val == root.val:
            return root

        if val < root.val:
            if root.left is not None:
                return self.FindVal(root.left, val)
            else:
                return None
        else:
            if root.right is not None:
                return self.FindVal(root.right, val)
            else:
                return None

    def FindMin(self, node):
        if node.left is not None:
            return self.FindMin(node.left)
        return node

    def RemoveMin(self, node):
        if node.left is None:
            if node.right is not None:
                node.right.parent = node
            return node.right
        
        node.left = self.RemoveMin(node.left)
        if node.left is not None:
            node.left.parent = node.left

        node = self.Rebalance(node) 
        return node
     
    def DelVal(self, root, val):
        if root is None:
            return None
        
        # DELETING ROOT !!!!!!!!!!!!!
        
        if val < root.val:
            root.left = self.DelVal(root.left, val)
        elif val > root.val:
            root.right = self.DelVal(root.right, val)
        else:
            if root.cnt > 0:
                root.cnt = root.cnt - 1
                return root
            
            q = root.left
            r = root.right
            
            if r is None:
                if q is not None:
                    q.parent = root.parent
                
                if root == self.tree_root:
                    self.tree_root = q
                return q

            min = self.FindMin(r)
            
            min.right = self.RemoveMin(r)
            r.parent = min
            
            min.left = q
            if q is not None:
                q.parent = min
            
            min.parent = root.parent
            
            if root == self.tree_root:
                self.tree_root = min
                
            #del root

            return self.Rebalance(min)
        return self.Rebalance(root)
        
    def PrintTree(self, root):
        if root is None:
            print "EMPTY!"
            return
    
        if root.left is not None:
            self.PrintTree(root.left)
        
        print root.val, root.height
        
        if root.right is not None:
            self.PrintTree(root.right)
            
    def SmallLeftRotation(self, node):
        b = node
        a = node.right

        a.parent = node.parent
        node.right = a.left

        if a.left is not None:
            (a.left).parent = node
        a.left = b

        if node.parent is not None:
            if node.parent.left == node:
                (node.parent).left = a
            else:
                (node.parent).right = a
            node.parent = a 
        else:
            node.parent = a
            self.tree_root = a

        self.FixHeight(b)
        self.FixHeight(a)
        return a
            
    def SmallRightRotation(self, node):
        a = node
        b = node.left

        b.parent = node.parent
        node.left = b.right
        
        if b.right is not None:
            (b.right).parent = a
        b.right = a
        
        if node.parent is not None: 
            if (node.parent).left == node:
                (node.parent).left = b
            else:
                (node.parent).right = b
            node.parent = b 
        else:
            node.parent = b
            self.tree_root = b
        
        self.FixHeight(a)
        self.FixHeight(b)
        return b
    
    def BigLeftRotation_slow(self, node):
        node.right = self.SmallRightRotation(node.right)
        node = self.SmallLeftRotation(node)
        return node
        
    def BigRightRotation_slow(self, node):
        node.left = self.SmallLeftRotation(node.left)
        node = self.SmallRightRotation(node)
        return node
        
    def BigLeftRotation_fast(self, node):
        a = node
        b = a.right
        c = b.left
        
        c.parent = a.parent

        if node.parent is not None: 
            if node.parent.left == a:
                node.parent.left = c
            else:
                node.parent.right = c
        else:
            node.parent = c
            self.tree_root = c

        if c.left is not None:
            c.left.parent = a

        a.parent = c
        a.right = c.left
        c.left = a

        if c.right is not None:
            c.right.parent = b

        b.parent = c
        b.left = c.right
        c.right = b
        
        self.FixHeight(a)
        self.FixHeight(b)
        self.FixHeight(c)
        return c
        
    def BigRightRotation_fast(self, node):
        a = node
        b = a.left
        c = b.right

        c.parent = a.parent
        
        if node.parent is not None: 
            if node.parent.left == a:
                node.parent.left = c
            else:
                node.parent.right = c
        else:
            node.parent = c
            self.tree_root = c
        
        if c.left is not None:
            c.left.parent = b

        b.parent = c
        b.right = c.left
        c.left = b

        if c.right is not None:
            c.right.parent = a

        a.parent = c
        a.left = c.right
        c.right = a
        
        self.FixHeight(a)
        self.FixHeight(b)
        self.FixHeight(c)
        return c

    def Rebalance(self, node):
        self.FixHeight(node)
        
        while (self.GetBalance(node)) >= 2:
            b = node.left
            if (self.GetHeight(b.right) <= self.GetHeight(b.left)):
                node = self.SmallRightRotation(node)
            else:
                node = self.BigRightRotation(node)
                
        while (self.GetBalance(node)) <= -2:
            a = node.right
            if (self.GetHeight(a.left) <= self.GetHeight(a.right)):
                node = self.SmallLeftRotation(node)
            else:
                node = self.BigLeftRotation(node)

        return node

# MAIN        

print "Working with random numbers"

t = AVL_Tree(None, False)
l = []

#sys.setrecursionlimit(10000) # program crashes with small numbers of this parameter

size = 100000 # size of tree
minrand = -10000 # minimum integer to generate as tree member
maxrand =  10000 # maximum integer to generate as tree member
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
    t.DelVal(t.tree_root, l[r])
    del l[r]
end_time = time.time() - start_time
print "Deleted %d random elements in: %0.5f" % (findsize, end_time)

start_time = time.time()
for i in xrange(size):
    r = random.randint(minrand, maxrand)
    l.append(r)
    t.AddVal(r)
end_time = time.time() - start_time
print "Added %d elements to the tree: %0.5f" % (size, end_time)

t = None
l = []
gc.collect() # just curious how it works =)
    
print
#sys.setrecursionlimit(10000) # program crashes with small numbers of this parameter
print "Working with increasing numbers, recursion limit:", sys.getrecursionlimit()
size = 100000
findsize = size // 20

t = AVL_Tree(None, False)
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
