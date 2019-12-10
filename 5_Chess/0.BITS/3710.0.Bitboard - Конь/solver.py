import sys
import string

# =====global vars=====
inpfile_ext = ".in"
solfile_ext = ".solve"
DEBUG = False
debugfile = "test.0.in"

# =====solver=====

def solve(inpdata):
    nA  = 0xFeFeFeFeFeFeFeFe
    nAB = 0xFcFcFcFcFcFcFcFc
    nH = 0x7f7f7f7f7f7f7f7f
    nGH = 0x3f3f3f3f3f3f3f3f

    knightBits = 1 << int(inpdata) 
    
    movesBits = nGH & (knightBits <<  6 | knightBits >> 10)
    movesBits = movesBits | nH & (knightBits << 15 | knightBits >> 17)
    movesBits = movesBits | nA  & (knightBits << 17 | knightBits >> 15)
    movesBits = movesBits | nAB & (knightBits << 10 | knightBits >>  6)
    
    c = 0
    t = movesBits
    while t != 0:
        c = c + (t & 1)
        t = t >> 1
    return c, movesBits

# =====main=====

if DEBUG:
    inpfile = debugfile
elif len(sys.argv) == 2:
    inpfile = sys.argv[1]
else:
    sys.exit("\n\nWrong args! Maybe running not from tester.py.")    

inpdata = open(inpfile, "r").read().rstrip('\n')
outdata = solve(inpdata)
outfile = inpfile.replace(inpfile_ext, solfile_ext)

with open(outfile, "w") as f:
    f.write(str(outdata[0]) + "\n" + str(outdata[1]) + "\n")

if DEBUG:
    print outdata[0]
    print outdata[1]
    
