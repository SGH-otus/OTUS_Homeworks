# -*- coding: utf-8 -*-
import struct

class RLE:
    description = "RLE compression algo"
    abbr = "R"
    
    def __init__(self):
        return None 

    def compress(self, inpdata):
        outdata = ""
        cntr = 0
        tmpstr = ""
        next_c = ""
        c = ""
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
            outdata = outdata + struct.pack("<b", cntr) + c
            
        return (len(outdata), outdata)

    def decompress(self, inpdata):
        outdata = ""
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
            
        return (len(outdata), outdata)
