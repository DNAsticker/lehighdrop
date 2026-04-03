from lehighdrop import Drop, Dir
import time
try:
    import pdclient
    client = pdclient.PdClient('http://localhost:7000/rpc')
except:
    client = None

if client != None:
    HV_SETTING_ID = 11
    HV_MAX = 190 #input('Enter voltage: ')
    client.set_parameter(HV_SETTING_ID, HV_MAX)

# initialize drop at top left and enable electrode underneath
dropA = Drop([0,2], [1,1], client)

#client.enable_positions([(0,2)])
dropA.activate()
time.sleep(1)

# Move the drop in a small circle
dropA.move(Dir.RIGHT)
time.sleep(1)

dropA.move(Dir.DOWN)
time.sleep(1)

dropA.move(Dir.LEFT)
time.sleep(1)

dropA.move(Dir.UP)
time.sleep(1)

if client != None:
    # turn off every electrode
    client.enable_positions([])
 
