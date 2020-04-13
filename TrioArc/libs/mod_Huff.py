# -*- coding: utf-8 -*-
import struct
import sys
import Queue as Q 
import bitstring

class Leaf:
    key = None
    val = None
    left = None
    right = None

    def __init__(self, val):
        self.val = val

    def EnumTree(self, prefix = bitstring.BitArray()):
        l = []
        if self.left:
            p2 = prefix.copy()
            p2.append("0b0")
            l.extend(self.left.EnumTree(p2))
        if self.val != None:
            l.append((prefix, self.val))
        if self.right:
            p2 = prefix.copy()
            p2.append("0b1")
            l.extend(self.right.EnumTree(p2))
        return l
    
    def SerializeTree(self):
        bs = bitstring.BitArray()
        if (self.left is None) and (self.right is None):
            bs.append("0b1")
            if ord(self.val) < 0x10:
                bs.append(hex(0))
            bs.append(hex(ord(self.val)))
        else:
            bs.append("0b0")
            if self.left:
                bs.append(self.left.SerializeTree())
            if self.right:
                bs.append(self.right.SerializeTree())
        return bs
       
    def DeserializeTree(self, lst):
        if len(lst) == 0:
            return None

        if int(lst.pop(0).bin) == 1:
            t = 0
            for i in range(8):
                t = t << 1
                t = t | int(lst.pop(0).bin)
            self.val = chr(t)
            return self
        else:
            l = Leaf(None)
            l.DeserializeTree(lst)
            r = Leaf(None)
            r.DeserializeTree(lst)
            self.left = l
            self.right = r
            return self

class Huffman:
    description = "Huffman compression algo"
    
    def __init__(self):
        return None 

    def compress(self, inpdata):
        dict = {}
        i = 0
        q = Q.PriorityQueue()

        while i < len(inpdata):
            if inpdata[i] in dict.keys():
                dict[inpdata[i]] += 1
            else:
                dict[inpdata[i]] = 1
            i = i + 1

        for i in dict.keys():
            dict[i] = dict[i] / 256.0
            l = Leaf(i)
            q.put((dict[i], l))

        while q.qsize() > 1:
            e1 = q.get()
            e2 = q.get()

            p = e1[0] + e2[0]
            l = Leaf(None)
            l.left = e1[1]
            l.right = e2[1]

            q.put((p, l))

        dict = {}
        root = q.get()
        for e in root[1].EnumTree():
            dict[e[1]] = e[0]
        s = root[1].SerializeTree()

        o = bitstring.BitArray()
        for c in inpdata:
            o.append(dict[c])
        
        outdata = struct.pack("<H", s.len)
        outdata = outdata + s.tobytes()
        outdata = outdata + struct.pack("<B", o.len % 8)
        outdata = outdata + o.tobytes()
        return (len(outdata), outdata)    

    def decompress(self, inpdata):
        tree_len = struct.unpack("<H", inpdata[0:2])[0]
        inpdata = inpdata[2:]

        tree_pad = tree_len % 8
        tree_len = tree_len //8
        if tree_pad != 0: 
            tree_len = tree_len + 1

        tree_data = inpdata[:tree_len]
        tree_bs = bitstring.BitArray(bytes = tree_data)[:tree_pad - 8]

        inpdata = inpdata[tree_len:]
        data_pad = struct.unpack("<B", inpdata[0])[0]

        inpdata = inpdata[1:]
        data_bs = bitstring.BitArray(bytes = inpdata)[:data_pad - 8]

        dict2 = {}
        root = Leaf(None)
        root.DeserializeTree(list(tree_bs.cut(1)))

        i = 0
        t = root
        s = ""

        while i < data_bs.len:
            if t.val is not None:
                s = s + t.val
                t = root
            else:
                if data_bs[i] == False:
                    t = t.left
                else:
                    t = t.right
                i = i + 1

        if t.val is not None:
            s = s + t.val

        return (len(s), s)    

