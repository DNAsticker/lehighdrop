from lehighdrop import Drop, Dir

class PurpleReg:

    # Initialize the registers. For now, this is assuming that the drops have been placed
    # in the correct positions.
    def __init__(self,  client, size = [2,2], registerCount = 5):
        self.size = size
        self.client = client
        self.registerCount = registerCount
        self.drops = []
        self.cur = 0
        self.drops.append(Drop([0,3], size, client))
        self.drops.append(Drop([3,3], size, client))
        self.drops.append(Drop([6,0], size, client))
        self.drops.append(Drop([3,0], size, client))
        self.drops.append(Drop([0,0], size, client))

        for drop in self.drops:
            drop.activate()

    # Wrapper function for moving a drop
    def Move(self, drop, dir) :
        # Don't attempt to move an empty drop
        if drop is None :
            return 
        return drop.move(dir) # may or may not need to return the 'move_drop' response object
    
    def MoveN(self, drop, dir, n) :
        for i in range(n):
            self.Move(drop, dir)

    def shiftCounterClockwise(self):
        # Move drop after cur into empty space 
        self.MoveN(self.drops[(self.cur+1)%self.registerCount], Dir.RIGHT, 3)
        # Move cur drop into empty space (created above) 
        self.MoveN(self.drops[(self.cur)%self.registerCount], Dir.RIGHT, 3)
        # Move drop furthest away from self.cur (the one above the new empty space) down
        self.MoveN(self.drops[(self.cur+4)%self.registerCount], Dir.DOWN, 3)
        # Move remaining leftmost top drop left
        self.MoveN(self.drops[(self.cur+3)%self.registerCount], Dir.LEFT, 3)
        # Move other top drop left
        self.MoveN(self.drops[(self.cur+2)%self.registerCount], Dir.LEFT, 3)
        # Move drop after self.cur up into empty space in top right 
        self.MoveN(self.drops[(self.cur+1)%self.registerCount], Dir.UP, 3)
        # Adjust new self.cur
        self.cur = (self.cur-1)%self.registerCount

    def shiftClockwise(self) :
        # Move top right drop into empty space
        self.MoveN(self.drops[(self.cur+2)%self.registerCount], Dir.DOWN, 3)
        # Move top middle drop into empty space to the right
        self.MoveN(self.drops[(self.cur+3)%self.registerCount], Dir.RIGHT, 3)
        # Move drop above self.cur to the right
        self.MoveN(self.drops[(self.cur+4)%self.registerCount], Dir.RIGHT, 3)
        # Move self.cur drop up
        self.MoveN(self.drops[(self.cur)%self.registerCount], Dir.UP, 3)
        # Move bottom middle drop into the self.cur spot
        self.MoveN(self.drops[(self.cur+1)%self.registerCount], Dir.LEFT, 3)
        # Move drop in empty space into spot just cleared up
        self.MoveN(self.drops[(self.cur+2)%self.registerCount], Dir.LEFT, 3)
        # Adjust new self.cur
        self.cur = (self.cur+1)%self.registerCount

    # Peek at a register value
    # Do NOT use this to get a drop to move it. Use getDrop instead.
    def checkRegister(self, target) :
        if target in range(self.registerCount):
            return self.drops[target]
        else:
            return None

    # Puts a drop into the right position and returns the Drop
    # object to the caller. 
    def getDrop(self, target) :
        if target in range(self.registerCount):
            # The faster dir is CW if target-cur = 0, 1, 2, -3, or -4
            CWRotationsNeeded = target - self.cur
            if CWRotationsNeeded in [0,1,2,-3,-4] :
                while (self.cur != target):
                    self.shiftClockwise()
            else :
                while (self.cur != target):
                    self.shiftCounterClockwise()
            # get the drop and remove it from the list
            drop = self.drops[self.cur]
            self.drops[self.cur] = None
            return drop # give the Drop object to the caller
        else:
            return None
        
    # Get direct access to the 3 easy to access drops
    # 
    # This should only be used if you don't plan on rotating
    # the shift register (you only need 3 drops)
    def getCacheDrop(self, target) :
        if target in range(3):
            target = ( target + self.cur ) % self.registerCount
            d = self.drops[target]
            self.drops[target] = None
            return d
        else:
            return None
        
    # These should only be used if you don't plan on rotating
    # the shift register (you only need 3 drops)
    def setCacheDrop(self, target, drop) :
        if target in range(3):
            target = ( target + self.cur ) % self.registerCount
            if self.drops[target] is not None :
                raise ValueError('Target register is full')
            self.drops[target] = drop
            return True
        else:
            return False
        
    # What follows is just an idea for how to insert a drop back into the 
    # register. There is probably a better way of doing this. 

    # This function should be called before moving a drop into the register
    # location for insertion. Returns True if successful, meaning the calling
    # code should move the drop into the register location and call insertDrop
    def prepareForInsertion(self, target) :
        if target in range(self.registerCount):
            # not sure if what protocol is for a full register or how overwriting would work
            if self.drops[target] is not None :
                raise ValueError('Target register is full')

            # The faster dir is CW if target-self.cur = 0, 1, 2, -3, or -4
            CWRotationsNeeded = target - self.cur
            if CWRotationsNeeded in [0,1,2,-3,-4] :
                while (self.cur != target):
                    self.shiftClockwise()
            else :
                while (self.cur != target):
                    self.shiftCounterClockwise()
            return True
        else :
            return False

    # Should only be called immediately after a successful call to prepareForInsertion
    # This puts the drop into the list and activates the electrodes under the drop (is that necessary?)
    def insertDrop(self, drop) :
        if self.drops[self.cur] is not None : 
            return False
        else :
            self.drops[self.cur] = drop
            self.drops[self.cur].activate()
            return True
    