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
        compressed_data = []

        for symbol in inpdata:
            string_plus_symbol = string + symbol
            if string_plus_symbol in dictionary: 
                string = string_plus_symbol
            else:
                compressed_data.append(dictionary[string])
                if(len(dictionary) <= self.maximum_table_size):
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_size += 1
                string = symbol

        if string in dictionary:
            compressed_data.append(dictionary[string])

        outdata = ""
        for data in compressed_data:
            outdata = outdata + pack('>H',int(data))
            
        return (len(outdata), outdata)    

    def decompress(self, inpdata):
        compressed_data = []
        next_code = 256
        decompressed_data = ""
        string = ""

        c = 0
        while c < len(inpdata):
            data = inpdata[c : c + 2]
            compressed_data.append(unpack('>H', data)[0])
            c = c + 2

        dictionary_size = 256
        dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])

        for code in compressed_data:
            if not (code in dictionary):
                dictionary[code] = string + (string[0])
            decompressed_data += dictionary[code]
            if not(len(string) == 0):
                dictionary[next_code] = string + (dictionary[code][0])
                next_code += 1
            string = dictionary[code]

        outdata = ""
        for data in decompressed_data:
            outdata = outdata + data

        return (len(outdata), outdata)  