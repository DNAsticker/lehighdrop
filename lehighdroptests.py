import lehighdrop
from lehighdrop import Drop, Dir
  
import time

try:
    import pdclient
    client = pdclient.PdClient('http://localhost:7000/rpc')
except:
    client = None



print('--------2x2 drop moves-----------')

lehighdrop.dropmat =[[' ','2','2',' ','4','4',' '],
          [' ','2','2',' ','4','4',' '],
          [' ',' ',' ',' ',' ',' ',' '],
          [' ','1','1',' ','3','3',' '],
          [' ','1','1',' ','3','3',' '],
          [' ',' ',' ',' ',' ',' ',' '],
          [' ',' ',' ',' ',' ',' ',' ']]

size = [2,2]
drops = []
drops.append(Drop([1,3], size, client))
drops.append(Drop([1,0], size, client))
drops.append(Drop([4,3], size, client))
drops.append(Drop([4,0], size, client))
for drop in drops:
    drop.activate()

drops[0].display()
drops[2].move_right()
drops[0].display()
drops[2].move_left()
drops[0].display()
drops[2].move_left()
drops[0].display()
drops[2].move_left()
drops[0].display()
drops[0].move_right()
drops[0].display()
drops[2].move_right()
drops[0].display()
drops[3].move_down()
drops[0].display()
drops[3].move_down()
drops[0].display()
drops[3].move_up()
drops[0].display()
drops[2].move_up()
drops[0].display()
drops[2].move_up()
drops[0].display()

print('--------1x1 drop moves-----------')

lehighdrop.dropmat =[[' ','2',' ','4',' '],
          [' ',' ',' ',' ',' '],
          [' ','1',' ','3',' '],
          [' ',' ',' ',' ',' '],
          [' ',' ',' ',' ',' ']]
client = None
size = [1,1]
drops = []
drops.append(Drop([1,2], size, client))
drops.append(Drop([1,0], size, client))
drops.append(Drop([3,2], size, client))
drops.append(Drop([3,0], size, client))
for drop in drops:
    drop.activate()

drops[0].display()
drops[2].move_right()
drops[0].display()
drops[2].move_left()
drops[0].display()
drops[2].move_left()
drops[0].display()
drops[2].move_left()
drops[0].display()
drops[0].move_right()
drops[0].display()
drops[2].move_right()
drops[0].display()
drops[3].move_down()
drops[0].display()
drops[3].move_down()
drops[0].display()
drops[3].move_up()
drops[0].display()
drops[2].move_up()
drops[0].display()
drops[2].move_up()
drops[0].display()

print('--------5 drop CSR-----------')

lehighdrop.dropmat =[['4','4',' ','3','3',' ','2','2',' ',' '],
          ['4','4',' ','3','3',' ','2','2',' ',' '],
          [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
          ['0','0',' ','1','1',' ',' ',' ',' ',' '],
          ['0','0',' ','1','1',' ',' ',' ',' ',' '],
          [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
          [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
          [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']]

global cur
cur = 0
size = [2, 2]
drops = []
drops.append(Drop([0,3], size, client))
drops.append(Drop([3,3], size, client))
drops.append(Drop([6,0], size, client))
drops.append(Drop([3,0], size, client))
drops.append(Drop([0,0], size, client))
#because of circular nature, drops index%5
for drop in drops:
    drop.activate()

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
def randomAccess(target):
    global cur
    if target in range(5):
        while (cur != target):
            shiftCounterClockwise()
        return True
    else:
        return False

print('drop number(0-4):',end='')
randomAccess(eval(input()))
drops[0].display()

print('--------9 drop CSR-----------')
lehighdrop.single_step=True

lehighdrop.dropmat =[['8',' ','7',' ','6',' ','5',' ',' ',' '],
          [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
          ['0',' ','1',' ','2',' ','3',' ','4',' '],
          [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
          [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
          [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']]

cur = 0
size = [1, 1]
registerCount = 9
drops = []
drops.append(Drop([0,2], size, client))
drops.append(Drop([2,2], size, client))
drops.append(Drop([4,2], size, client))
drops.append(Drop([6,2], size, client))
drops.append(Drop([8,2], size, client))
drops.append(Drop([6,0], size, client))
drops.append(Drop([4,0], size, client))
drops.append(Drop([2,0], size, client))
drops.append(Drop([0,0], size, client))
#because of circular nature, drops index%registerCount
for drop in drops:
    drop.activate()

def Move(drop, dir) :
    # Don't attempt to move an empty drop
    if drop is None :
        return 
    return drop.move(dir) # may or may not need to return the 'move_drop' response object

def shiftCounterClockwise():
    global cur,drops
    # Move drop into empty space 
    Move(drops[(cur+4)%registerCount], Dir.UP)
    Move(drops[(cur+4)%registerCount], Dir.UP)
    # Shift drops 0-3 to the right
    Move(drops[(cur+3)%registerCount], Dir.RIGHT)
    Move(drops[(cur+3)%registerCount], Dir.RIGHT)
    # Shift drops 0-3 to the right
    Move(drops[(cur+2)%registerCount], Dir.RIGHT)
    Move(drops[(cur+2)%registerCount], Dir.RIGHT)
    # Shift drops 0-3 to the right
    Move(drops[(cur+1)%registerCount], Dir.RIGHT)
    Move(drops[(cur+1)%registerCount], Dir.RIGHT)
    # Shift drops 0-3 to the right
    Move(drops[(cur)%registerCount], Dir.RIGHT)
    Move(drops[(cur)%registerCount], Dir.RIGHT)
    # Move drop into the cur slot 
    Move(drops[(cur+8)%registerCount], Dir.DOWN)
    Move(drops[(cur+8)%registerCount], Dir.DOWN)
    # Shift drops 4-7 to the left
    Move(drops[(cur+7)%registerCount], Dir.LEFT)
    Move(drops[(cur+7)%registerCount], Dir.LEFT)
    # Shift drops 4-7 to the left
    Move(drops[(cur+6)%registerCount], Dir.LEFT)
    Move(drops[(cur+6)%registerCount], Dir.LEFT)
    # Shift drops 4-7 to the left
    Move(drops[(cur+5)%registerCount], Dir.LEFT)
    Move(drops[(cur+5)%registerCount], Dir.LEFT)
    # Shift drops 4-7 to the left
    Move(drops[(cur+4)%registerCount], Dir.LEFT)
    Move(drops[(cur+4)%registerCount], Dir.LEFT)
    # Adjust new cur
    cur = (cur-1)%registerCount

def shiftClockwise() :
    global cur,drops
    # Shift drops 8-5 to the right
    Move(drops[(cur+5)%registerCount], Dir.RIGHT)
    Move(drops[(cur+5)%registerCount], Dir.RIGHT)
    # Shift drops 8-5 to the right
    Move(drops[(cur+6)%registerCount], Dir.RIGHT)
    Move(drops[(cur+6)%registerCount], Dir.RIGHT)
    # Shift drops 8-5 to the right
    Move(drops[(cur+7)%registerCount], Dir.RIGHT)
    Move(drops[(cur+7)%registerCount], Dir.RIGHT)
    # Shift drops 8-5 to the right
    Move(drops[(cur+8)%registerCount], Dir.RIGHT)
    Move(drops[(cur+8)%registerCount], Dir.RIGHT)
    # Move cur up into top row
    Move(drops[(cur)%registerCount], Dir.UP)
    Move(drops[(cur)%registerCount], Dir.UP)
    # Shift drops 1-4 to the left
    Move(drops[(cur+1)%registerCount], Dir.LEFT)
    Move(drops[(cur+1)%registerCount], Dir.LEFT)
    # Shift drops 1-4 to the left
    Move(drops[(cur+2)%registerCount], Dir.LEFT)
    Move(drops[(cur+2)%registerCount], Dir.LEFT)
    # Shift drops 1-4 to the left
    Move(drops[(cur+3)%registerCount], Dir.LEFT)
    Move(drops[(cur+3)%registerCount], Dir.LEFT)
    # Shift drops 1-4 to the left
    Move(drops[(cur+4)%registerCount], Dir.LEFT)
    Move(drops[(cur+4)%registerCount], Dir.LEFT)
    # drop 5 down to free empty space 
    Move(drops[(cur+5)%registerCount], Dir.DOWN)
    Move(drops[(cur+5)%registerCount], Dir.DOWN)
    # Adjust new cur
    cur = (cur+1)%registerCount

# Puts a drop into the right position and returns the Drop
# object to the caller. 
def getDrop(target) :
    global cur
    if target in range(registerCount):
        # The faster dir is CW if target-cur = 0, 1, 2, -3, or -4
        CWRotationsNeeded = target - cur
        if CWRotationsNeeded in [0,1,2,3,4,-5,-6,-7,-8] :
            while (cur != target):
                shiftClockwise()
        else :
            while (cur != target):
                shiftCounterClockwise()
        # get the drop and remove it from the list
        drop = drops[cur]
        drops[cur] = None
        return drop # give the Drop object to the caller
    else:
        return None
    
print('drop number(0-8):',end='')
drops[cur] = getDrop(eval(input()))
drops[0].display()

