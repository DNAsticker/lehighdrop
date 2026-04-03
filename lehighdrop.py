#supports a subset of operations of pdclient Drop class
# in addition uses global variables
#  lehighdrop.dropmat:     matrix of char to identify each drop for simulation
#  lehighdrop.single_step: boolean that causes pause after each simulation step when True
#  lehighdrop.verbose:     boolean that causes debugging output after each simulation step when True

single_step = True 
verbose = True

try:
    import pdclient
    if verbose:
        print("pdclient installed")
except:
    if verbose:
        print("pdclient not installed, simulation only")

# by default, assume empty misl_v4_1 board

dropmat        =[[' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                 [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
                 ['*','*','*','*',' ',' ','*','*','*','*'],
                 ['*','*','*','*',' ',' ','*','*','*','*'],
                 ['*','*','*','*',' ',' ','*','*','*','*'],
                 ['*','*','*','*',' ',' ','*','*','*','*']]

try:
    from pdclient.drop import Dir
except:
    class Dir:
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4
    if verbose:
        print("lehigh Dir class")

def dir2str(dir):
    if dir == Dir.UP:
        return "Up"
    elif dir == Dir.DOWN:
        return "Down"
    elif dir == Dir.LEFT:
        return "Left"
    elif dir == Dir.RIGHT:
        return "Right"

class Drop:
    def __init__(self,pos,size,client):
        global dropmat
        self.x = pos[0]
        self.y = pos[1]
        self.sizex = size[0]
        self.sizey = size[1]
        #print('Drop('+str(pos)+str(size)+')=')
        #for offy in range(self.sizey):
        #    for offx in range(self.sizex):
        #        print(dropmat[self.y+offy][self.x+offx],end='')
        #    print('')
        self.client = client
        if self.client != None:
            self.actual = pdclient.drop.Drop(pos,size,self.client)
    def activate(self): #in simulation, creates visible drops for unlabeled locations
        for offy in range(self.sizey):
            for offx in range(self.sizex):
                if dropmat[self.y+offy][self.x+offx] == ' ':
                    dropmat[self.y+offy][self.x+offx]='@'  #placeholder for unlabeled drop
        if verbose:
            if self.client != None:
                print(' actual',end=' ')
            print('activate')
            self.display()
        if self.client != None:
            return self.actual.activate()
        else:
            return None
    def pins(self):     #stub
        if self.client != None:
            return self.actual.pins()
        else:
            return None #simulator does not consider pins
    def move(self,dir):
        if dir == Dir.UP:
            self.move_up()
        elif dir == Dir.DOWN:
            self.move_down()
        elif dir == Dir.LEFT:
            self.move_left()
        elif dir == Dir.RIGHT:
            self.move_right()
    def move_right(self):
        for offy in range(self.sizey):
            #print(self.y+offy)
            #print(self.x)
            if dropmat[self.y+offy][self.x+self.sizex] != ' ':
                print('right error')
                return
            else:
                dropmat[self.y+offy][self.x+self.sizex] = dropmat[self.y+offy][self.x]
                dropmat[self.y+offy][self.x] = ' '
        self.x = self.x + 1
        if verbose:
            print('right')
            self.display()
        if self.client != None:
            return self.actual.move_right()
    def move_left(self):
        for offy in range(self.sizey):
            if dropmat[self.y+offy][self.x-1] != ' ':
                print('left error')
                return
            else:
                dropmat[self.y+offy][self.x-1] = dropmat[self.y+offy][self.x]
                dropmat[self.y+offy][self.x+self.sizex-1] = ' '
        self.x = self.x - 1
        if verbose:
            print('left')
            self.display()
        if self.client != None:
            return self.actual.move_left()
    def move_up(self):
        for offx in range(self.sizex):
            if dropmat[self.y-1][self.x+offx] != ' ':
                print('up error')
                return
            else:
                dropmat[self.y-1][self.x+offx] = dropmat[self.y][self.x+offx]
                dropmat[self.y+self.sizey-1][self.x+offx] = ' '
        self.y = self.y - 1
        if verbose:
            print('up')
            self.display()
        if self.client != None:
            return self.actual.move_up()
    def move_down(self):
        for offx in range(self.sizex):
            if dropmat[self.y+self.sizey][self.x+offx] != ' ':
                print('down error')
                return
            else:
                dropmat[self.y+self.sizey][self.x+offx] = dropmat[self.y][self.x+offx]
                dropmat[self.y][self.x+offx] = ' '
        self.y = self.y + 1
        if verbose:
            print('down')
            self.display()
        if self.client != None:
            return self.actual.move_down()
    #display is only in simulation
    def display(self):
        global dropmat
        for i in range(0,len(dropmat[0])+2):
                print('*',end='')
        print('**')
        for row in dropmat:
           print('**',end='')
           for drop in row:
               print(drop, end='')
           print('**')
        if single_step:
            input()



