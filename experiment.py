"""
Experiment 4
At appropriate locations on Purple Drop, place a 4uL drop of pure buffer solution, a 4uL drop of
unhybridized data strand (only 000), and a 4 uL drop of probe/Iron bead. Run a python script
that implements the separate operation. (Depending on results of Iron-bead-only experiments
to be conducted prior to arrival of the DNA, the magnet operations may be implemented
automatically by the electromagnet or by manual placing and removing the Neodymium
magnet when instructed by the python script.) Illuminate these drops in a darkened room with
the appropriate UV light, and observe whether the expected drop is visible (take a picture). Set
aside the drops for EM imaging.

Experiment 5
At appropriate locations on Purple Drop (probably the CSR locations), place three distinct 4uL
drop of pure buffer solution, a 4uL drop of hybridized data strand (a mix of 000 and 001 from
Experiment 2), and a 4 uL drop of probe0/Iron bead. Run a python script that implements three
separate operations (one separates 000 from 001; the other two separate again making the tag
visibly indicate that the separation occurred). Illuminate these drops in a darkened room with
the appropriate UV light, and observe whether the expected drop is visible (take a picture). Set
aside the drops for EM imaging.

Experiment 6
This experiment tests the automatic setting of a bit (rather than doing it manually as in
Experiment 2). At appropriate locations on Purple Drop (probably the CSR locations), place a
4uL drop of unhybridized data strand (000), a 4 uL drop of sticker0, a 4 uL drop of probe0/Iron
bead and a 4 uL drop of probe0/Iron bead. Run a python script that implements three separate
operations (the first separates 000 using probe0 into the drop that contains sticker0; the
second separates the 001 resulting from hybridization using probe 1, the middle bit known to
be 0, to isolate it from excess stickers; the third lets the tag show that all the data strands are
001). Illuminate these drops in a darkened room with the appropriate UV light, and observe
whether the expected drop is visible (take a picture). Set aside the drops for EM imaging.
"""

import lehighdrop
from lehighdrop import Drop,Dir
# import heater
import purpleReg
import time

try:
    import pdclient
    client = pdclient.PdClient('http://localhost:7000/rpc')
except:
    client = None
    heat = None 

# Get our heater and register objects
heat = None # heater.get_v4_1_controller(client)
register = purpleReg.PurpleReg(client, size = [2,2], registerCount=5)

# location of heater opening
OPENING_Y = 7
OPENING_X = 4

# Maximum temperature we will allow the heater to be set to
MAX_TEMP = 80 

# location where target is returned
global returnx,returny

# move target from cache line to heater
#
# drop is a Drop object
def moveTargetToHeater(drop):
    global returnx,returny
    # save return address
    returnx = drop.x
    returny = drop.y
    # Move drop down to bottom row
    while(drop.y != OPENING_Y):
        drop.move_down()
    # Move drop over opening to heater  
    while(drop.x != OPENING_X):
        if drop.x < OPENING_X:
            drop.move_right()
        else:
            drop.move_left()
    # Move drop down into heater  
    for i in range(0,4):
        drop.move_down()

# move target back to cache line
def moveHeaterToTarget(drop):
    # Move drop up to bottom row
    while drop.y != OPENING_Y:
        drop.move_up()
    # Move drop over opening to heater  
    while(drop.x != returnx):
        if drop.x < returnx:
            drop.move_right()
        else:
            drop.move_left()
    # Move drop up and back to CSR  
    while(drop.y != returny):
        drop.move_up()

# Perform a split in the heater area, having the user manually hold a 
# magnet over the area.
def coldMagSplit(drop) :
    print("Position magnet over heater area and then hit return")
    input()

    drop.move_up()
    drop.move_up()

    print("Split complete.")


# temp is the target tempature in Celsius
# timeAtTemp is how long to block for when the drop reaches the target temperature
# tempErrorRange is the acceptable range for the timer to start in Celcius
#
# e.g. hotMagSplit(45, 10, .5) would hold the block for 10 seconds once the
# drop temperature reaches 44.5 C
def hotMagSplit(drop, temp, timeAtTemp, tempErrorRange = 0) :
    if temp >= MAX_TEMP : 
        raise ValueError("target temperature exceeds maximum temperature of",MAX_TEMP)
    
    # Set the target and start heating
    heat.set_target(temp)
    heat.start()
    print("Starting heater, target:",temp)
    
    # Wait for it to heat up
    # TODO consider max and min range, not just assume it will heat up from below
    while heat.drop_temperature < (temp - tempErrorRange) :
        pass

    # block for set amount of time
    print("Waiting for",timeAtTemp,"seconds")
    time.sleep(timeAtTemp)

    # Wait for user to apply magnet
    print("Position magnet over heater area and then hit return")
    input()

    # Split the drop while heater and magnet are on
    for i in range(0,2):
        drop.move_up()
    
    print("Finished. Stopping heater")
    heat.stop()
    return True


# tube1, tube2, probe all Drop objects, probably just retrieved from cache line
def separate(tube1, tube2, probe, heaterTemp, timeInHeater) :
    # Put dry probes in heater area
    moveTargetToHeater(probe)
    coldMagSplit(probe)
    moveHeaterToTarget(probe)

    # move tube1 to heater area, mix with probes
    moveTargetToHeater(tube1)
    coldMagSplit(tube1) 
    moveHeaterToTarget(tube1)

    # move tube2 to heater area, do hot magnetic split
    moveTargetToHeater(tube2)
    hotMagSplit(tube2, heaterTemp, timeInHeater)
    moveHeaterToTarget(tube2)

    input("Consider waiting for heater to cool down before rehydrating probe. Press enter to move on...")

    # probe rehydrates
    moveTargetToHeater(probe)
    moveHeaterToTarget(probe)

def experiment4() :
    print("Please place drops like such:")
    print("1: 4uL drop of pure buffer solution")
    print("2: 4uL drop of unhybridized data strand (only 000)")
    print("3: 4uL drop of probe0/Iron bead")
    print('************\n*      33  *\n*      33  *\n*          *\n*11 22     *\n*11 22     *\n*          *')
    print('*          *\n*          *\n*****  *****\n*****  *****\n*****  *****\n*****  *****\n************')

    input("Press Enter when done...")

    # The user should have placed the drops in the specified location, and there are only three drops
    # So, we just use the cache locations to avoid using the shift register
    pureBuffer = register.getCacheDrop(0)
    dataStrand = register.getCacheDrop(1)
    probe = register.getCacheDrop(2)

    # Perform separate. 
    # after this, dataStrand should be pureBuffer
    # pureBuffer should be the datastrand
    separate(dataStrand, pureBuffer, probe, 55, 10)

    # the separate operation would have moved all the drops back to
    # the cache line, so for good practice we reinsert in cache
    register.setCacheDrop(0, pureBuffer)
    register.setCacheDrop(1, dataStrand)
    register.setCacheDrop(2, probe)

    print("(Ideal) Expected Results:")
    print("1: 4uL drop of unhybridized data strand (only 000)")
    print("2: 4uL drop of pure buffer solution")
    print("3: 4uL drop of probe0/Iron bead")
    print('************\n*      33  *\n*      33  *\n*          *\n*11 22     *\n*11 22     *\n*          *')
    print('*          *\n*          *\n*****  *****\n*****  *****\n*****  *****\n*****  *****\n************')

    print("Experiment Finished")

def experiment5() :
    print("Please place drops like such:")
    print("1: 4uL drop of hybridized data strand (a mix of 000 and 001 from Experiment 2) ")
    print("2: 4uL drop of probe0/Iron bead")
    print("3: 4uL drop of pure buffer solution")
    print("4: 4uL drop of pure buffer solution")
    print("5: 4uL drop of pure buffer solution")
    print('************\n*55 44 33  *\n*55 44 33  *\n*          *\n*11 22     *\n*11 22     *\n*          *')
    print('*          *\n*          *\n*****  *****\n*****  *****\n*****  *****\n*****  *****\n************')

    input("Consider using dashboard to adjust as necessary. Press Enter when done...")

    # For the first separate operation, we will use them in the cache locations
    dataStrand = register.getCacheDrop(0)
    probe = register.getCacheDrop(1)
    pureBuffer1 = register.getCacheDrop(2)

    # Perform separate. 
    # dataStrand will become just 000
    # pureBuffer1 will become 001
    separate(dataStrand, pureBuffer1, probe, 55, 10)
    
    # Put the drops back in the cache line
    register.setCacheDrop(0, dataStrand)
    register.setCacheDrop(1, probe)
    register.setCacheDrop(2, pureBuffer1)

    # Now we will use the CSR to shift and allow us to use the cache line again
    # NB: not a great way of doing this, but it's a start

    # Second separate operation to verify 001 (previously called pureBuffer1)

    # This will shift so that the probe is in cache0, 
    register.shiftClockwise()
    probe = register.getCacheDrop(0)
    data001 = register.getCacheDrop(1)
    pureBuffer2 = register.getCacheDrop(2)

    # Perform separate.
    # data001 will become 001
    # pureBuffer2 will stay pure
    separate(data001, pureBuffer2, probe, 55, 10)

    # Put the drops back in the cache line
    register.setCacheDrop(0, probe)
    register.setCacheDrop(1, data001)
    register.setCacheDrop(2, pureBuffer2)

    # Third separate operation to verify 000 (previously called dataStrand)

    # Shift such that cache0 is pureBuffer
    # cache1 is data 000
    # cache2 is probe
    register.shiftCounterClockwise()
    register.shiftCounterClockwise()

    pureBuffer3 = register.getCacheDrop(0)
    data000 = register.getCacheDrop(1)
    probe = register.getCacheDrop(2)

    # Perform separate.
    # data000 will become pure buffer
    # pureBuffer3 will become 000
    separate(data000, pureBuffer3, probe, 55, 10)

    # Put the drops back in the cache line
    register.setCacheDrop(0, pureBuffer3)
    register.setCacheDrop(1, data000)
    register.setCacheDrop(2, probe)


    print("(Ideal) Expected Results:")
    print("1: 4uL drop of just 000 data strand")
    print("2: 4uL drop of pure buffer solution")
    print("3: 4uL drop of probe0/Iron bead")
    print("4: 4uL drop of just 001 data strand")
    print("5: 4uL drop of pure buffer solution")
    print('************\n*55 44 33  *\n*55 44 33  *\n*          *\n*11 22     *\n*11 22     *\n*          *')
    print('*          *\n*          *\n*****  *****\n*****  *****\n*****  *****\n*****  *****\n************')


    print("Experiment Finished")


def experiment6() :
    print("Please place drops like such:")
    print("1: 4uL drop of unhybridized data strand (000)")
    print("2: 4uL ddrop of sticker0")
    print("3: 4uL drop of probe0/Iron bead")
    print("4: 4uL drop of pure Buffer solution")
    print("5: 4uL drop of probe1/Iron bead")
    print('************\n*55 44 33  *\n*55 44 33  *\n*          *\n*11 22     *\n*11 22     *\n*          *')
    print('*          *\n*          *\n*****  *****\n*****  *****\n*****  *****\n*****  *****\n************')

    input("Consider using dashboard to adjust as necessary. Press Enter when done...")

    data000 = register.getCacheDrop(0)
    sticker0 = register.getCacheDrop(1)
    probe0 = register.getCacheDrop(2)

    # Perform separate.
    # sticker0 becomes data 001 with excess sticker0
    # data000 become pure buffer
    separate(data000, sticker0, probe0, 55, 10)

    # Put the drops back in the cache line
    register.setCacheDrop(0, data000)
    register.setCacheDrop(1, sticker0)
    register.setCacheDrop(2, probe0)

    # Now we will use the CSR to shift and allow us to use the cache line again
    register.shiftCounterClockwise()
    
    probe1 = register.getCacheDrop(0)
    pureBuffer = register.getCacheDrop(1)
    data001 = register.getCacheDrop(2)

    # Perform separate.
    # data001 becomes excess sticker0
    # pureBuffer becomes data001
    separate(data001, pureBuffer, probe1, 55, 10)

    # Put the drops back in the cache line
    register.setCacheDrop(0, probe1)
    register.setCacheDrop(1, pureBuffer)
    register.setCacheDrop(2, data001)

    # we want to get the data strand, but keep it out of the way of the CSR.
    # the three drops we need are not sequential, so can't use the cache line how we have been
    register.shiftCounterClockwise()
    data001 = register.getCacheDrop(2)
    register.MoveN(data001, Dir.DOWN, 6)
    register.Move(data001, Dir.RIGHT)

    register.shiftCounterClockwise()

    probe0 = register.getCacheDrop(0)
    pureBuffer = register.getCacheDrop(1)

    # Perform separate.
    # data001 becomes data 001
    # pureBuffer becomes pure buffer
    separate(data001, pureBuffer, probe0, 55, 10)

    # Put the drops back in the cache line
    register.setCacheDrop(0, probe0)
    register.setCacheDrop(1, pureBuffer)

    register.shiftClockwise()
    register.Move(data001, Dir.LEFT)
    register.MoveN(data001, Dir.UP, 6)
    register.setCacheDrop(2, data001)

    print("(Ideal) Expected Results:")
    print("1: 4uL drop of pure buffer solution")
    print("2: 4uL ddrop of probe1/Iron bead")
    print("3: 4uL drop of data strand 001")
    print("4: 4uL drop of excess sticker 0")
    print("5: 4uL drop of probe0/Iron bead")
    print('************\n*55 44 33  *\n*55 44 33  *\n*          *\n*11 22     *\n*11 22     *\n*          *')
    print('*          *\n*          *\n*****  *****\n*****  *****\n*****  *****\n*****  *****\n************')

    print("Experiment Finished")

