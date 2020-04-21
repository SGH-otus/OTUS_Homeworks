# -*- coding: utf-8 -*-
import argparse
import sys
import os
import struct
import shutil
import time

MODE_DECOMPRESS = "D"
MODE_LIST1 = "L1"
MODE_LIST2 = "L2"
MODE_ONE_OBJ = "O"

signature = "TRAR"

modules = []

from libs import mod_RLE as MR
modules.append(MR.RLE())

from libs import mod_Huff as MH
modules.append(MH.Huffman())

from libs import mod_LZW as ML
modules.append(ML.LZW())

# TODOs:
# - CRCs
# - CRYPTO
# - verbose?
# - rmtree?

def file_pack(fpath, algo):
    #print fpath
    fname = fpath.split('\\')[-1]
    f = open(fpath, "rb")
    fdata = f.read()
    len(fdata)
    f.close()
   
    s = ""
    (fsize, c_data) = algo.compress(fdata)
    s = s + struct.pack("<H", len(fname)) 
    s = s + struct.pack("<I", fsize) 
    s = s + fname
    s = s + c_data
    return (s, len(fdata))

def dir_pack(arc_path, algo):
    data = b""
    sz = 0
    lst = os.listdir(arc_path)
    for fname in lst[:]:
        path = os.path.join(arc_path, fname)
        if os.path.isdir(path):
            data = data + struct.pack("<H", (0x8000 | len(fname))) + fname
            (t_s, t_sz) = dir_pack(path, algo)
            data = data + t_s
            sz = sz + t_sz
            lst.remove(fname)
            
    for fname in lst:
        (p1, p2) = file_pack(os.path.join(arc_path, fname), algo)
        data = data + p1
        sz = sz + p2
    return (data + struct.pack("<H", 0), sz)
       
def read_arc(start, algo, tree, mode, mode_params):
    while True:
        c = tree[start + 0 : start + 2]
        c = struct.unpack("<H", c)[0]
        start = start + 2
        
        if c == 0:
            return start
        else:
            if (c & 0x8000):
                namelen = c & 0x7FFF
                fname = tree[start : start + namelen] + "\\"
                start = start + namelen
                newdir_name = mode_params[0] + fname

                if mode == MODE_ONE_OBJ:
                    if newdir_name == mode_params[1]:
                        if not os.path.exists(newdir_name):
                            os.mkdir(newdir_name)
                        read_arc(start, algo, tree, MODE_DECOMPRESS, [".\\" + fname])
                    else:
                        start = read_arc(start, algo, tree, mode, [newdir_name, mode_params[1]])
                if mode == MODE_LIST1:
                    print newdir_name
                    start = read_arc(start, algo, tree, mode, [mode_params[0] + "   "])
                if mode == MODE_LIST2:
                    start = read_arc(start, algo, tree, mode, [newdir_name])
                if mode == MODE_DECOMPRESS:
                    if not os.path.exists(newdir_name):
                        os.mkdir(newdir_name)
                    start = read_arc(start, algo, tree, mode, [newdir_name])

            else:
                namelen = c & 0x7FFF
                fsize = tree[start : start + 4]
                fsize = struct.unpack("<I", fsize)[0]
                fname = tree[start + 4  : start + 4 + namelen]
                fdata = tree[start + 4 + namelen : start + 4 + namelen + fsize]

                fname_full = mode_params[0] + fname

                if mode == MODE_ONE_OBJ:
                    if fname_full == mode_params[1]:
                        (d_fsize, d_data) = algo.decompress(fdata)
                        with open(".\\" + fname, "wb") as f: f.write(d_data); f.close();
                if mode == MODE_LIST1:
                   print fname_full
                if mode == MODE_LIST2:
                   print fname_full
                if mode == MODE_DECOMPRESS:    
                    #print fname_full
                    (d_fsize, d_data) = algo.decompress(fdata)
                    with open(fname_full, "wb") as f: f.write(d_data); f.close();

                start = start + 4 + namelen + fsize
    return None            

parser = argparse.ArgumentParser(description = "TrioArc archiver", add_help = False)
   
group1 = parser.add_argument_group(title="Actions group", description="One of these options must be chosen.")
group2 = group1.add_mutually_exclusive_group(required = True)
group2.add_argument("-c", "--compress", help = "Compress file", action = "store_true")
group2.add_argument("-d", "--decompress", help = "Decompress file", action = "store_true")
group2.add_argument("-d1", "--decompress_one", help = "Extract one object", action = "store_true")
group2.add_argument("-l1", "--list1", help = "List archive contents, tree", action = "store_true")
group2.add_argument("-l2", "--list2", help = "List archive contents, full paths", action = "store_true")
group2.add_argument("-b", "--benchmark", help = "Benchmark available compressing algorithms on choosen data", action = "store_true")
group2.add_argument("-a", "--algos", help = "List available compressing algorithms", action = "store_true")
group1.add_argument("-algo", required = False, metavar = "A", help = "Algorithm to compress with (Default - RLE)")
group1.add_argument("-inp", required = False, metavar = "path", help = "Input path")
group1.add_argument("-out", required = False, metavar = "path", help = "Output path (Default - \"archive.trar\" / <current_dir>)")
group1.add_argument("-objname", required = False, metavar = "name", help = "Object name (only with -d1)")

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

if args.algos:
    print "Shortcut : Description"
    for a in modules:
        print a.abbr, "       :", a.description
    
elif args.compress:
    cur_algo = None
    if args.algo:
        for m in modules:
            if m.abbr == args.algo:
                cur_algo = m

        if cur_algo == None:
            parser.error('Unknown algorithm!')
    else:
        parser.error('Algorithm type required to comperss data!')

    if not args.inp:
        parser.error('Input path required for this action!')
    
    fnm = "archive.trar"
    if args.out:
        fnm = args.out

    start_time = time.time()

    if os.path.isdir(args.inp):
        (data, size) = dir_pack(args.inp, cur_algo)
    else: 
        (data, size) = file_pack(args.inp, cur_algo)
        data = data + struct.pack("<H", 0)

    end_time = time.time() - start_time
    print "COMPRESSION DONE in %0.2f s. Ratio %0.2f (%d / %d bytes)" % (end_time, (1.0 * len(data)) / size, len(data), size)

    data = signature + cur_algo.abbr + data
    with open(fnm, "wb") as f: f.write(data); f.close();
    print "Output file:", fnm
    
elif args.decompress:
    if not args.inp:
        parser.error('Input path required for this action!')

    with open(args.inp, "rb") as f: inpdata = f.read(); f.close();
    if inpdata[:4] != signature:
        print "ERROR: WRONG SIGNATURE"
        exit(-1)

    cur_algo = None
    for a in modules:
        if a.abbr == inpdata[4]:
            cur_algo = a

    if cur_algo == None:
        print "ERROR: WRONG ALGO"
        exit(-1)

    inpdata = inpdata[5:]

    out_path = ".\\"
    if args.out:
        out_path = args.out

    if out_path[:-1] != "\\":
        out_path = out_path + "\\"

    if not os.path.exists(out_path):
        os.mkdir(out_path)
       
    start_time = time.time()

    read_arc(0, cur_algo, inpdata, MODE_DECOMPRESS, [out_path])
 
    end_time = time.time() - start_time
    print "Decompressed in %0.2f s." % (end_time)
 

elif args.benchmark:
    if not args.inp:
        parser.error('Input path required for this action!')

    for a in modules:
        print a.description, ":", 

        start_time = time.time()

        if os.path.isdir(args.inp):
            (data, size) = dir_pack(args.inp, a)
        else: 
            (data, size) = file_pack(args.inp, a)

        end_time = time.time() - start_time
        print "%0.2f s. Ratio %0.2f (%d / %d bytes)" % (end_time, (1.0 * len(data)) / size, len(data), size)
    
elif args.list1:
    if not args.inp:
        parser.error('Input path required for this action!')

    with open(args.inp, "rb") as f: inpdata = f.read(); f.close();
    if inpdata[:4] != signature:
        print "ERROR: WRONG SIGNATURE"
        exit(-1)

    cur_algo = None
    for a in modules:
        if a.abbr == inpdata[4]:
            cur_algo = a

    if cur_algo == None:
        print "ERROR: WRONG ALGO"
        exit(-1)

    inpdata = inpdata[5:]
    read_arc(0, cur_algo, inpdata, MODE_LIST1, [""])

elif args.list2:
    if not args.inp:
        parser.error('Input path required for this action!')

    with open(args.inp, "rb") as f: inpdata = f.read(); f.close();
    if inpdata[:4] != signature:
        print "ERROR: WRONG SIGNATURE"
        exit(-1)

    cur_algo = None
    for a in modules:
        if a.abbr == inpdata[4]:
            cur_algo = a

    if cur_algo == None:
        print "ERROR: WRONG ALGO"
        exit(-1)

    inpdata = inpdata[5:]
    read_arc(0, cur_algo, inpdata, MODE_LIST2, [""])

elif args.decompress_one:
    if not args.inp:
        parser.error('Input path required for this action!')

    if not args.objname:
        parser.error('Object name required for this action!')

    with open(args.inp, "rb") as f: inpdata = f.read(); f.close();
    if inpdata[:4] != signature:
        print "ERROR: WRONG SIGNATURE"
        exit(-1)

    cur_algo = None
    for a in modules:
        if a.abbr == inpdata[4]:
            cur_algo = a

    if cur_algo == None:
        print "ERROR: WRONG ALGO"
        exit(-1)

    inpdata = inpdata[5:]
    read_arc(0, cur_algo, inpdata, MODE_ONE_OBJ, ["", args.objname])
