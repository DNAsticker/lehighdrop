import lehighdrop
from lehighdrop import Drop, Dir
  
import time

try:
    import pdclient
    client = pdclient.PdClient('http://localhost:7000/rpc')
except:
    client = None



print('--------5 drop CSR-----------')

lehighdrop.dropmat[0:5] =[['4','4',' ','3','3',' ','2','2',' ',' '],
                          ['4','4',' ','3','3',' ','2','2',' ',' '],
                          [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                          ['0','0',' ','1','1',' ',' ',' ',' ',' '],
                          ['0','0',' ','1','1',' ',' ',' ',' ',' ']]

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
dropnum = eval(input())
while dropnum in range(0,5):
    randomAccess(dropnum)
    print('drop number(0-4):',end='')
    dropnum = eval(input())


