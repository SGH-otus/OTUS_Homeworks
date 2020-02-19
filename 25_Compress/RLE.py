# -*- coding: utf-8 -*-
import argparse
import struct
import sys

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

inpdata = open(args.file, "rb").read()
outdata = ""

if args.compress:
    cntr = 0
    tmpstr = ""
    next_c = ""
    i = 0
    
    while i < len(inpdata) - 1:
        c = inpdata[i]
        next_c = inpdata[i + 1]

        if (c != next_c):
            if (cntr == -126):
                outdata = outdata + struct.pack("<b", cntr) + tmpstr
                cntr = 0
                tmpstr = ""
            elif (cntr <= 0):
                cntr = cntr - 1
                tmpstr = tmpstr + c
            elif (cntr > 0):
                outdata = outdata + struct.pack("<b", cntr) + c
                cntr = 0
                i = i + 1

        if (c == next_c):    
            if (cntr == 127):
                outdata = outdata + struct.pack("<b", cntr - 1) + c
                cntr = 0
            elif (cntr >= 0):
                cntr = cntr + 1
            elif (cntr < 0):
                outdata = outdata + struct.pack("<b", cntr) + tmpstr
                cntr = 1
                tmpstr = ""

        if cntr not in (0,1):
            i = i + 1
    
    if tmpstr != "":
        outdata = outdata + struct.pack("<b", cntr - 1) + tmpstr + next_c
    else:
        outdata = outdata + struct.pack("<b", cntr + 1) + c
    
    outdata = "RLE" + outdata
    
    open(args.file + ".rle", "wb").write(outdata)

else: 
    if inpdata[:3] != "RLE":
        print "SIGNATURE ERROR"
        exit(-1)
    
    inpdata = inpdata[3:]
    
    c = 0
    while c < len(inpdata):
        n = struct.unpack("<b", inpdata[c])[0]
        c = c + 1
        if n > 0:
            outdata = outdata + inpdata[c] * n
            c = c + 1
        else:
            outdata = outdata + inpdata[c:c+(-n)]
            c = c + (-n)
    open(args.file + ".unrle", "wb").write(outdata)

"""
Сравнить работу программы с разными типами файлов и составить сравнительную таблицу: текст, фото, аудио, zip-архив и написать вывод. + 2 байта 

Вариант А. Алгоритм RLE. 
1. Написать функции сжатия и распаковки массива по улучшенному алгоритму RLE. + 4 байта 
2. Написать программу для сжатия файла. + 2 байта 
3. Написать программу для распаковки файла. + 2 байта. 
"""