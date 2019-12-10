import sys
import string

# =====global vars=====
inpfile_ext = ".in"
solfile_ext = ".solve"
DEBUG = False
debugfile = "test.1.in"

# =====solver vars=====

figures = "PNBRQKpnbrqk"

# =====solver=====

def parse_line(line, f):
    r = 0
    for c in line:
        if c in string.digits:
            r = r << int(c)
        elif c == f:
            r = (r << 1) | 1 
        else: 
            r = r << 1
    return r 

def solve(inpdata):
    state = {}

    data = inpdata.split("/")
    for f in figures:
        t = 0
        for i in range(len(data)):
            t = (t << 8) + parse_line(data[i][::-1], f)
        state[f] = t
    return state

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
    for fig in figures:
        f.write(str(outdata[fig]) + "\n")

if DEBUG:
    print
    print '\n'.join(['%s: %s' % (key, value) for (key, value) in outdata.items()])
