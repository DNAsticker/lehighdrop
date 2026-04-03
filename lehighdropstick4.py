import lehighdrop
from lehighdrop import Drop,Dir


print('--------5 drop CSR-----------')

lehighdrop.dropmat =[[' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                 ['4','4',' ','3','3',' ','2','2',' ',' '],
                 ['4','4',' ','3','3',' ','2','2',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                 ['0','0',' ','1','1',' ',' ',' ',' ',' '],
                 ['0','0',' ','1','1',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                 ['*','*','*','*',' ',' ','*','*','*','*'],
                 ['*','*','*','*',' ',' ','*','*','*','*'],
                 ['*','*','*','*',' ',' ','*','*','*','*'],
                 ['*','*','*','*',' ',' ','*','*','*','*']]

global cur
cur = 0
client = None
size = [2, 2]
drops = []
drops.append(Drop([0,4], size, client))
drops.append(Drop([3,4], size, client))
drops.append(Drop([6,1], size, client))
drops.append(Drop([3,1], size, client))
drops.append(Drop([0,1], size, client))
#because of circular nature, drops index%5

drops[0].display()


lehighdrop.single_step=True

def shiftCounterClockwise():
    global cur,drops
    # Move drop after cur into empty space 
    drops[(cur+1)%5].move_right()
    drops[(cur+1)%5].move_right()
    drops[(cur+1)%5].move_right()
    # Move cur drop into empty space (created above) 
    drops[cur].move_right()
    drops[cur].move_right()
    drops[cur].move_right()
    # Move drop furthest away from cur (the one above the new empty space) down
    drops[(cur+4)%5].move_down()
    drops[(cur+4)%5].move_down()
    drops[(cur+4)%5].move_down()
    # Move remaining leftmost top drop left
    drops[(cur+3)%5].move_left()
    drops[(cur+3)%5].move_left()
    drops[(cur+3)%5].move_left()
    # Move other top drop left
    drops[(cur+2)%5].move_left()
    drops[(cur+2)%5].move_left()
    drops[(cur+2)%5].move_left()
    # Move drop after cur up into empty space in top right 
    drops[(cur+1)%5].move_up()
    drops[(cur+1)%5].move_up()
    drops[(cur+1)%5].move_up()
    # Adjust new cur
    cur = (cur-1)%5

# not as efficient as choosing clockwise/counterclockwise based on distance
# uses cur,(cur+1)%5 and (cur+2)%5 as cache line

def randomAccess(target):
    global cur
    if target in range(5):
 #      while (cur != target):
        while ((target-cur)%5>2) :
            shiftCounterClockwise()
        return True
    else:
        return False

# location of heater opening
OPENING_Y = 7
OPENING_X = 4

# location where target is returned
global returnx,returny


# move target from cache line to heater

def moveTargetToHeater(target):
    global cur,drops
    global returnx,returny
    # save return address
    returnx = drops[target].x
    returny = drops[target].y
    # Move drop down to bottom row
    while(drops[target].y != OPENING_Y):
        drops[target].move_down()
    # Move drop over opening to heater  
    while(drops[target].x != OPENING_X):
        if drops[target].x < OPENING_X:
            drops[target].move_right()
        else:
            drops[target].move_left()
    # Move drop down into heater  
    for i in range(0,4):
        drops[target].move_down()

# move target back to cache line

def moveHeaterToTarget(target):
    global cur,drops
    # Move drop up to bottom row
    for i in range(0,4):
        drops[target].move_up()
    # Move drop over opening to heater  
    while(drops[target].x != returnx):
        if drops[target].x < returnx:
            drops[target].move_right()
        else:
            drops[target].move_left()
    # Move drop up and back to CSR  
    while(drops[target].y != returny):
        drops[target].move_up()

# the symbolic id (one char) of contents of drop corresponding to tube number

def tubeid(tubeno):
    return lehighdrop.dropmat[drops[tubeno].y][drops[tubeno].x]

# the symbolic id (one char) of contents of drop in heater 

def heaterid():
    return lehighdrop.dropmat[12][4]

# test of random access only

print('drop number(0-4):',end='')
dropaddr = eval(input())
while dropaddr != -1:
    randomAccess(dropaddr)
    moveTargetToHeater(dropaddr)
    moveHeaterToTarget(dropaddr)
    for i in range(0,5):
        print('i='+str(i),end=' ')
        print(tubeid(i))
    drops[0].display()
    print('drop number(0-4):',end='')
    dropaddr = eval(input())

# simulation of heater/magnet/probe/sticker interaction given drop contents

#----------------------
STICK = 0      #index into list for free STICKer; for bit i a[STICK] is 2^i used by bitset manip
PROBE = 1      #index into list for free PROBE;   for bit i a[PROBE] is 2^i used by bitset manip
STRAND = 2     #a[STRAND] is list of ints (possible dups) representing data strand;each int is bitset of >=0 kinds of stickers on that strand
VOL   = 3      #a[VOL] is volume of water containing the strands; 1.0 is "ideal" drop size
tiny = 0.015   #relative volume held by dry probes
evap = 0.001   #relative volume lost to evaporation during heating 

# set up a drop that contains data strands passed in l; there may be dups representing redundant strands

def initial_strands(l):
    if len(l) > 0:
        return [0, 0, l, 1.0]
    else:
        return [0, 0, [], 1.0]

# set up a drop that contains only free stickers for bit i

def initial_stick(i):
    return [1<<i, 0, [], 1.0]

# set up a drop that contains only free probes for bit i

def initial_probe(i):
    return [0, 1<<i, [], 1.0]


# one drop into two whose volumes are given by ratio
# assumes volume is relatively large enough compare to molecule size that
# at least one copy of each free sticker, free probe and strand exists in both copies

def split(a,ratio):
    return ([a[STICK],a[PROBE],a[STRAND],      ratio*a[VOL]],
            [a[STICK],a[PROBE],a[STRAND],(1.0-ratio)*a[VOL]])

# mix two drops a and b, forming one drop whose volume is their sum
# This results in three things:
# 1. the union of the set of data strands (the "+" in "for" is concat of the two lists,a[STRAND] and b[STRAND])
# 2. we assume enough stickers so every data strand is forced to hybridize with free stickers from either input (s|a[STICK]|b[STICK])
# 3. the free stickers and probes are also ORed together

def mix(a,b):
    r = []
    for s in a[STRAND]+b[STRAND]:
        r.append(s|a[STICK]|b[STICK])
    return [ a[STICK]|b[STICK], a[PROBE]|b[PROBE], r, a[VOL]+b[VOL]]

#
# model the sticker "combine" of two drops, a and b
# returns two drops: the mix of a and b, and an "empty drop" where b used to be

def combine_a(a,b):
    return (mix(a,b), [0, 0, [], 0.0])

# with magnet turned on and heater off, split one drop into:
# 1. most of the water containing all free stickers, and all strands that have stickers hybridized to selected bit position
# 2. a tiny residue of water with free probes and those strands that probes hybridize to (ie
#    the ones that don't have stickers in selected bit positions) being held stationary by a magnet

def coldMagSplit(a):
    r0 = []
    r1 = []
    for s in a[STRAND]:
      if s&a[PROBE]:
        r1.append(s)
      else:
        r0.append(s)
    #return ( [a[STICK], 0, r1, a[VOL]-tiny],   [0, a[PROBE], r0, tiny] )
    return ( [a[STICK], 0, r1, a[VOL]*(1-tiny)],   [0, a[PROBE], r0, a[VOL]*tiny] )


# with magnet and heater turned on,  split one drop into:
# 1. most of the water containing all free stickers and all strands (which can't hybridize to probes but still have their stickers)
# 2. a tiny residue of water with only free probes (all of the probes because they can't hybridize)

def hotMagSplit(a):
    #return ( [a[STICK], 0, a[STRAND], a[VOL]-tiny], [0, a[PROBE], [], tiny] )
    return ( [a[STICK], 0, a[STRAND], a[VOL]*(1-evap)*(1-tiny)], [0, a[PROBE], [], a[VOL]*(1-evap)*tiny] )


#----------------------

def separate_b(t0, t1, p0):

    # x held by magnet for following 3 steps

    p0,x = coldMagSplit(p0)# x is almost dry after p0 removed
    x = mix(x,t0)          # hybridize move to heater/magnet 
    t0,x = coldMagSplit(x) # x is almost dry after t0 removed
    x = mix(x,t1)          # t1 rehydrates 
    t1,x = hotMagSplit(x)  # x is almost dry after t1 removed

    # x released from magnet

    p0 = mix(x,p0)         # p0 rehydrates; move out of heater/magnet
    return (t0, t1, p0)


def showt(t0,t1,p0,p1,s2):
    print('t0=',end='')
    print(t0)
    print('t1=',end='')
    print(t1)
    print('p0=',end='')
    print(p0)
    print('p1=',end='')
    print(p1)
    print('s2=',end='')
    print(s2)

T0 = 0
T1 = 1
P0 = 4
P1 = 3
S2 = 2
contents = dict()
contents[tubeid(T0)] = initial_strands([0,1,2,3])
contents[tubeid(T1)] = initial_strands([])
contents[tubeid(S2)] = initial_stick(2)
contents[tubeid(P0)] = initial_probe(0)
contents[tubeid(P1)] = initial_probe(1)
print(contents)
input()

def display_contents():
    for i in range(0,5):
        print(str(i)+'='+str(contents[str(i)]))

def separateNovel(t0,t1,p0):
    randomAccess(p0)
    moveTargetToHeater(p0)
    contents[heaterid()],x = coldMagSplit(contents[heaterid()])# x is almost dry after contents of heater removed
    moveHeaterToTarget(p0)

    randomAccess(t0)
    moveTargetToHeater(t0)
    x = mix(x,contents[heaterid()])          # hybridize move to heater/magnet 
    contents[heaterid()],x = coldMagSplit(x) # x is almost dry after t0 removed
    moveHeaterToTarget(t0)

    randomAccess(t1)
    moveTargetToHeater(t1)
    x = mix(x,contents[heaterid()])          # t1 rehydrates 
    contents[heaterid()],x = hotMagSplit(x)  # x is almost dry after t1 removed
    moveHeaterToTarget(t1)

    randomAccess(p0)
    moveTargetToHeater(p0)
    contents[heaterid()] = mix(x,contents[heaterid()])         # p0 rehydrates; move out of heater/magnet
    moveHeaterToTarget(p0)
    display_contents()

def xorNovel():
    separateNovel(T0,T1,P0)
    separateNovel(T0,S2,P1)
    separateNovel(T1,T0,P1)
    separateNovel(T1,S2,P0)
    separateNovel(S2,T0,P1)
    separateNovel(S2,T0,P0)

xorNovel()

def test_c():
    print('------------------')
    t0=initial_strands([0,1,2,3])
    t1=initial_strands([])
    s2=initial_stick(2)
    p0=initial_probe(0)
    p1=initial_probe(1)
    showt(t0,t1,p0,p1,s2)
    t0,t1,p0 = separate_b(t0,t1,p0)
    showt(t0,t1,p0,p1,s2)
    t0,s2,p1 = separate_b(t0,s2,p1)
    showt(t0,t1,p0,p1,s2)
    t1,t0,p1 = separate_b(t1,t0,p1)
    showt(t0,t1,p0,p1,s2)
    print('instead of combine')
    t1,s2,p0 = separate_b(t1,s2,p0)
    showt(t0,t1,p0,p1,s2)
    s2,t0,p1 = separate_b(s2,t0,p1)
    showt(t0,t1,p0,p1,s2)
    s2,t0,p0 = separate_b(s2,t0,p0)
    showt(t0,t1,p0,p1,s2)

#test_c()

