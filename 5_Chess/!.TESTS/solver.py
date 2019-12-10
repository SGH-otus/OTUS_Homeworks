import sys

# =====global vars=====
inpfile_ext = ".in"
solfile_ext = ".solve"

DEBUG = False
debugfile = "test.0.in"

# =====solver=====

def solve(inpdata):
    outdata = len(inpdata)
    return outdata


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
open(outfile, "w").write(str(outdata))

if DEBUG:
    print str(outdata)

  


