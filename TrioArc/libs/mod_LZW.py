import struct
from struct import *

class LZW:
    description = "LZW compression algo"
    abbr = "L"
    maximum_table_size = 2**16-1
    
    def __init__(self):
        return None 

    def compress(self, inpdata):
        dictionary_size = 256                   
        dictionary = {chr(i): i for i in range(dictionary_size)}    
        string = ""
        outdata = ""

        for symbol in inpdata:
            string_plus_symbol = string + symbol
            if string_plus_symbol in dictionary: 
                string = string_plus_symbol
            else:
                outdata = outdata + pack('>H', dictionary[string])
                if(len(dictionary) <= self.maximum_table_size):
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_size += 1
                string = symbol

        if string in dictionary:
            outdata = outdata + pack('>H', dictionary[string])

        return (len(outdata), outdata)    

    def decompress(self, inpdata):
        dictionary_size = 256
        dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])
        next_code = 256
        string = ""
        outdata = ""

        c = 0
        while c < len(inpdata):
            code = unpack('>H', inpdata[c : c + 2])[0]
            if not (code in dictionary):
                dictionary[code] = string + string[0]
            #decompressed_data += dictionary[code]
            outdata = outdata + dictionary[code]
            if not(len(string) == 0):
                dictionary[next_code] = string + dictionary[code][0]
                next_code += 1
            string = dictionary[code]
            c = c + 2

        return (len(outdata), outdata)  