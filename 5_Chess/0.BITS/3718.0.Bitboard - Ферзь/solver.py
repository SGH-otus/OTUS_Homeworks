import sys
import string
import math

# =====global vars=====
inpfile_ext = ".in"
solfile_ext = ".solve"
DEBUG = False
USE_MASKS = True
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

def parse_state(inpdata):
    state = {}

    data = inpdata.split("/")
    for f in figures:
        t = 0
        for i in range(len(data)):
            t = (t << 8) + parse_line(data[i][::-1], f)
        state[f] = t
    return state

def bitscan_forward(n): # in ASM there is specian instructions for this - BSF/BSR
    i = 1
    while( (n >> i) % 2 == 0):
        i += 1
    return i

def bitscan_reverse(n): # in ASM there is specian instructions for this - BSF/BSR
    i = 1
    while( ((n << i) & 0x8000000000000000) == 0):
        i += 1
    return 63 - i

def solve_rookie_masks(bits, allWhites, allBlacks):
    RookieBits = bits 
    
    c1 = int(math.log(RookieBits, 256)) # TODO: is log worth it? or mb do this through cycles
    c2 = int(math.log((RookieBits >> (8 * c1) & 255), 2))
    
    movesBits_V = 0x0101010101010101 << c2 # TODO: is masks worth it? or mb do this through cycles
    movesBits_V = movesBits_V ^ RookieBits # get rid of current pos
    movesBits_H = 0xff << (8 * c1)
    movesBits_H = movesBits_H ^ RookieBits

    # OLD SOLUTION
    """
    movesBits_V = 0x0101010101010101
    while movesBits_V & RookieBits == 0: # TODO: is it worth to make it with masks, without cycle?
        movesBits_V = movesBits_V << 1
    
    movesBits_H = 0xff
    while movesBits_H & RookieBits == 0:
        movesBits_H = movesBits_H << 8
    """
    
    movesBits = movesBits_V | movesBits_H
    
    blockers_white = allWhites & movesBits
    blockers_black = allBlacks & movesBits
    blockers_all = blockers_white | blockers_black

    #movesBits_down = movesBits_V & ((RookieBits >> c1) - 1) # TODO: try to get rid of RookieBits (maybe like Bishop?)
    movesBits_down = movesBits_V & ((256**c1) - 1)
    movesBits_up = (movesBits_V ^ movesBits_down)

    #movesBits_left = movesBits_H & (RookieBits - 1)
    movesBits_left = movesBits_H & (0x0101010101010101 * (2**c2 - 1))
    movesBits_right = (movesBits_H ^ movesBits_left) 

    #up
    if movesBits_up != 0:
        blockers_up = movesBits_up & blockers_all
        if blockers_up == 0: 
            real_movesBits_up = movesBits_up
        else:
            first_blocker_up = (1 << bitscan_forward(blockers_up))
            real_movesBits_up = ((0xffffffffffffffff - ((first_blocker_up << 1) - 1)) & movesBits_up) ^ movesBits_up 
            if (first_blocker_up & blockers_white) != 0:
                real_movesBits_up = real_movesBits_up ^ first_blocker_up
    else:
        real_movesBits_up = 0

    #down
    if movesBits_down != 0:
        blockers_down = movesBits_down & blockers_all
        if blockers_down == 0: 
            real_movesBits_down = movesBits_down
        else:
            first_blocker_down = (1 << bitscan_reverse(blockers_down))
            real_movesBits_down = 0xffffffffffffffff - ((first_blocker_down << 0) - 1 ) & movesBits_down
            if (first_blocker_down & blockers_white) != 0:
                real_movesBits_down = real_movesBits_down ^ first_blocker_down
    else:
        real_movesBits_down = 0

    #right
    if movesBits_right != 0:
        blockers_right =  movesBits_right & blockers_all
        if blockers_right == 0: 
            real_movesBits_right = movesBits_right
        else:
            first_blocker_right = (1 << bitscan_forward(blockers_right))
            real_movesBits_right = ((first_blocker_right << 1) - 1 ) & movesBits_right
            if (first_blocker_right & blockers_white) != 0:
                real_movesBits_right = real_movesBits_right ^ first_blocker_right
    else:
        real_movesBits_right = 0

    #left
    if movesBits_left != 0:
        blockers_left = movesBits_left & blockers_all
        if blockers_left == 0: 
            real_movesBits_left = movesBits_left
        else:
            first_blocker_left = (1 << bitscan_reverse(blockers_left))
            real_movesBits_left = (0xffffffffffffffff - (first_blocker_left - 1)) & movesBits_left
            if (first_blocker_left & blockers_white) != 0:
                real_movesBits_left = real_movesBits_left ^ first_blocker_left
    else:
        real_movesBits_left = 0
        
    real_movesBits = real_movesBits_up | real_movesBits_down | real_movesBits_right | real_movesBits_left

    return real_movesBits 

def solve_rookie_cycles(bits, allWhites, allBlacks):
    RookieBits = bits 
    
    c1 = int(math.log(RookieBits, 256)) # TODO: is log worth it? or mb do this through cycles
    c2 = int(math.log((RookieBits >> (8 * c1) & 255), 2))
    
    # RookieBits = 256**c1 << c2 
    
    #up
    real_movesBits_up = 0
    t = RookieBits << 8
    while t < 0xffffffffffffffff:
        if t & allWhites:
            break
        if t & allBlacks:
            real_movesBits_up = real_movesBits_up | t
            break
        real_movesBits_up = real_movesBits_up | t
        t = t << 8
    
    #down
    real_movesBits_down = 0
    t = RookieBits
    while t > 0:
        t = t >> 8
        if t & allWhites:
            break
        if t & allBlacks:
            real_movesBits_down = real_movesBits_down | t
            break
        real_movesBits_down = real_movesBits_down | t
    
    #right
    real_movesBits_right = 0
    t = RookieBits << 1
    while t < 256**(c1 + 1):
        if t & allWhites:
            break
        if t & allBlacks:
            real_movesBits_right = real_movesBits_right | t
            break
        real_movesBits_right = real_movesBits_right | t
        t = t << 1
    
    #left
    real_movesBits_left = 0
    t = RookieBits >> 1
    while t >= 256**c1:
        if t & allWhites:
            break
        if t & allBlacks:
            real_movesBits_left = real_movesBits_left | t
            break
        real_movesBits_left = real_movesBits_left | t
        t = t >> 1
   
    real_movesBits = real_movesBits_up | real_movesBits_down | real_movesBits_right | real_movesBits_left

    return real_movesBits 

def solve_bishop_masks(bits, allWhites, allBlacks):
    BishopBits = bits
    
    c1 = int(math.log(BishopBits, 256)) # TODO: is log worth it? or mb do this through cycles
    c2 = int(math.log((BishopBits >> (8 * c1) & 255), 2))
    
    #NOT ALWAYS WORKING (mb not enough precision in negative powers)
    #movesBits_L = 0xffffffffffffffff & int(0x0102040810204080 * 256**(c1 + c2 - 7)) # TODO: is masks worth it? or mb do this through cycles
    #movesBits_R = 0xffffffffffffffff & int(0x8040201008040201 * 256**(c1 - c2))
    
    # some workaround with shifts
    movesBits_L = 0xffffffffffffffff & ((0x0102040810204080 << 56) >> (56 + 8 * (7 - c1 - c2))) # TODO: is masks worth it? or mb do this through cycles
    movesBits_R = 0xffffffffffffffff & ((0x8040201008040201 << 56) >> (56 + 8 * (c2 - c1)))
    
    movesBits = movesBits_L ^ movesBits_R

    blockers_white = allWhites & movesBits
    blockers_black = allBlacks & movesBits
    blockers_all = blockers_white | blockers_black

    up = 0xffffffffffffffff & (0xffffffffffffffff << (8 * (c1 + 1)))
    down = 0xffffffffffffffff & (~up)
    right = 0xffffffffffffffff & (~(0x0101010101010101 * (2**(c2 + 1) - 1)))
    left = 0xffffffffffffffff & (~right)

    movesBits_UL = movesBits & up & left
    movesBits_UR = movesBits & up & right
    movesBits_DL = movesBits & down & left
    movesBits_DR = movesBits & down & right

    # up-left
    if movesBits_UL != 0:
        blockers_UL = movesBits_UL & blockers_all
        if blockers_UL == 0: 
            real_movesBits_UL = movesBits_UL
        else:
            first_blocker_UL = (1 << bitscan_forward(blockers_UL))
            real_movesBits_UL = ((0xffffffffffffffff - ((first_blocker_UL << 1) - 1)) & movesBits_UL) ^ movesBits_UL 
            if (first_blocker_UL & blockers_white) != 0:
                real_movesBits_UL = real_movesBits_UL ^ first_blocker_UL
    else:
        real_movesBits_UL = 0

    # up-right
    if movesBits_UR != 0:
        blockers_UR = movesBits_UR & blockers_all
        if blockers_UR == 0: 
            real_movesBits_UR = movesBits_UR
        else:
            first_blocker_UR = (1 << bitscan_forward(blockers_UR))
            real_movesBits_UR = ((0xffffffffffffffff - ((first_blocker_UR << 1) - 1)) & movesBits_UR) ^ movesBits_UR 
            if (first_blocker_UR & blockers_white) != 0:
                real_movesBits_UR = real_movesBits_UR ^ first_blocker_UR
    else:
        real_movesBits_UR = 0

    # down-left
    if movesBits_DL != 0:
        blockers_DL = movesBits_DL & blockers_all
        if blockers_DL == 0: 
            real_movesBits_DL = movesBits_DL
        else:
            first_blocker_DL = (1 << bitscan_reverse(blockers_DL))
            real_movesBits_DL = ((0xffffffffffffffff - ((first_blocker_DL << 0) - 1)) & movesBits_DL)
            if (first_blocker_DL & blockers_white) != 0:
                real_movesBits_DL = real_movesBits_DL ^ first_blocker_DL
    else:
        real_movesBits_DL = 0

    # down-right
    if movesBits_DR != 0:
        blockers_DR = movesBits_DR & blockers_all
        if blockers_DR == 0: 
            real_movesBits_DR = movesBits_DR
        else:
            first_blocker_DR = (1 << bitscan_reverse(blockers_DR))
            real_movesBits_DR = ((0xffffffffffffffff - ((first_blocker_DR << 0) - 1)) & movesBits_DR)
            if (first_blocker_DR & blockers_white) != 0:
                real_movesBits_DR = real_movesBits_DR ^ first_blocker_DR
    else:
        real_movesBits_DR = 0

    real_movesBits = real_movesBits_UL | real_movesBits_UR | real_movesBits_DL | real_movesBits_DR
    
    return real_movesBits   
    
def solve_bishop_cycles(bits, allWhites, allBlacks):
    BishopBits = bits
    
    c1 = int(math.log(BishopBits, 256)) # TODO: is log worth it? or mb do this through cycles
    c2 = int(math.log((BishopBits >> (8 * c1) & 255), 2))
    
    #up-left
    real_movesBits_UL = 0
    t = BishopBits
    while (t & 0xFF00000000000000 == 0) and (t & 0x0101010101010101 == 0):
        t = t << 7
        if t & allWhites:
            break
        if t & allBlacks:
            real_movesBits_UL = real_movesBits_UL | t
            break
        real_movesBits_UL = real_movesBits_UL | t
   
   #up-right
    real_movesBits_UR = 0
    t = BishopBits
    while (t & 0xFF00000000000000 == 0) and (t & 0x8080808080808080 == 0):
        t = t << 9
        if t & allWhites:
            break
        if t & allBlacks:
            real_movesBits_UR = real_movesBits_UR | t
            break
        real_movesBits_UR = real_movesBits_UR | t
   
    #down-left
    real_movesBits_DL = 0
    t = BishopBits
    while (t & 0x00000000000000FF == 0) and (t & 0x0101010101010101 == 0):
        t = t >> 9
        if t & allWhites:
            break
        if t & allBlacks:
            real_movesBits_DL = real_movesBits_DL | t
            break
        real_movesBits_DL = real_movesBits_DL | t
        
    #down-right
    real_movesBits_DR = 0
    t = BishopBits
    while (t & 0x00000000000000FF == 0) and (t & 0x8080808080808080 == 0):
        t = t >> 7
        if t & allWhites:
            break
        if t & allBlacks:
            real_movesBits_DR = real_movesBits_DR | t
            break
        real_movesBits_DR = real_movesBits_DR | t    
   
    real_movesBits = real_movesBits_UL | real_movesBits_UR | real_movesBits_DL | real_movesBits_DR
    real_movesBits = real_movesBits
    
    return real_movesBits      

if USE_MASKS:
    solve_rookie = solve_rookie_masks
    solve_bishop = solve_bishop_masks
else:
    solve_rookie = solve_rookie_cycles
    solve_bishop = solve_bishop_cycles
  
def solve_queen(bits, allWhites, allBlacks):
    QueenBits = bits
    
    real_movesBits = solve_bishop(QueenBits, allWhites, allBlacks) | solve_rookie(QueenBits, allWhites, allBlacks)
   
    return real_movesBits    
    
def solve(inpdata):
    state = parse_state(inpdata)

    allWhites = 0
    for c in "PNBRQK":
        allWhites = allWhites | state[c]

    allBlacks = 0
    for c in "pnbrqk":
        allBlacks = allBlacks | state[c]

    bits = int(state['R'])
    bitsRookie = solve_rookie(bits, allWhites, allBlacks)
    
    bits = int(state['B']) 
    bitsBishop = solve_bishop(bits, allWhites, allBlacks)

    bits = int(state['Q']) 
    bitsQueen = solve_queen(bits, allWhites, allBlacks)
    
    return bitsRookie, bitsBishop, bitsQueen

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
    f.write(str(outdata[0]) + "\n")
    f.write(str(outdata[1]) + "\n")
    f.write(str(outdata[2]) + "\n")

if DEBUG:
    print
    print outdata[0]
    print outdata[1]
    print outdata[2]
    
