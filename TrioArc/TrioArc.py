# -*- coding: utf-8 -*-
import argparse
import sys
import os
import struct
import shutil

sys.path.append(".\\libs")

modules = []

from mod_RLE import RLE
modules.append(RLE())

from mod_Huff import Huffman
modules.append(Huffman())

cur_mod = modules[0]

#for m in modules:
#    print m.description
    

'''
parser = argparse.ArgumentParser(description="RLE compress/decompress")
   
group1 = parser.add_argument_group(title="Actions group", description="One of these options must be chosen.")
group2 = group1.add_mutually_exclusive_group(required=True)
group2.add_argument("-c", "--compress", help="Compress file", action="store_true")
group2.add_argument("-d", "--decompress", help="Decompress file", action="store_true")
parser.add_argument("file", help="Filename to work with")
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()


if args.compress:
    print "COMPRESS"
    print args.file

'''

# LIST ARCHIVE CONTENTS
# EXTRACT ONLY ONE ITEM

def make_tree(walk_path):
    s = b""
    lst = os.listdir(walk_path)
    for fname in lst[:]:
        path = os.path.join(walk_path, fname)
        if os.path.isdir(path):
            s = s + struct.pack("<H", (0x8000 | len(fname))) + fname
            s = s + make_tree(path)
            lst.remove(fname)
            
    for fname in lst:
        f = open(os.path.join(walk_path, fname), "rb")
        fdata = f.read()
        f.close()
       
        (fsize, c_data) = cur_mod.compress(fdata)
        s = s + struct.pack("<H", len(fname)) 
        s = s + struct.pack("<I", fsize) 
        s = s + fname
        s = s + c_data
    return s + struct.pack("<H", 0)
       
def read_tree(start, tree, out_path):
    while True:
        c = tree[start + 0 : start + 2]
        c = struct.unpack("<H", c)[0]
        start = start + 2
        
        if c == 0:
            return start
        else:
            if (c & 0x8000):
                namelen = c & 0x7FFF
                fname = tree[start : start + namelen]
                start = start + namelen
                os.mkdir(out_path + fname + "\\")
                start = read_tree(start, tree, out_path + fname + "\\")
            else:
                namelen = c & 0x7FFF
                fsize = tree[start : start + 4]
                fsize = struct.unpack("<I", fsize)[0]
                fname = tree[start + 4  : start + 4 + namelen]
                fdata = tree[start + 4 + namelen : start + 4 + namelen + fsize]
                (d_fsize, d_data) = cur_mod.decompress(fdata)
                with open(out_path + fname, "wb") as f: f.write(d_data); f.close();
                start = start + 4 + namelen + fsize

walk_path = "C:\\Work\\TrioArc\\test"
tree = make_tree(walk_path)

with open("arc", "wb") as f: f.write(tree); f.close();

print "COMPRESSION DONE"

out_path = "C:\\Work\\TrioArc\\test2"

if out_path[:-1] != "\\":
    out_path = out_path + "\\"

if os.path.exists(out_path):
    shutil.rmtree(out_path)
os.mkdir(out_path)
   
read_tree(0, tree, out_path)



