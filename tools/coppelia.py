import sim
import sys
from math import floor, degrees, sin, cos
import numpy
from numpy import array

def coppelia():
    # From https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i+n]

    # Open a connection and get all the shapes ------------------------------------
    sim.simxFinish(-1)  # just in case, close all opened connections
    client_id = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)  # Connect to CoppeliaSim 
    if client_id != -1:
        print('Robot connected')
    else:
        sys.exit('Connection failed')

    # Get cuboids ------------------------------
    result, cuboids_handle = sim.simxGetCollectionHandle(client_id, "cuboids", sim.simx_opmode_blocking)
    result, handles, _, floatData, _ = sim.simxGetObjectGroupData(client_id, cuboids_handle, 9, sim.simx_opmode_blocking)
    cuboids = array(list(chunks(floatData, 6)))

    # Get cylinders ----------------------------
    result, cylinders_handle = sim.simxGetCollectionHandle(client_id, "cylinders", sim.simx_opmode_blocking)
    result, handles, _, floatData, _ = sim.simxGetObjectGroupData(client_id, cylinders_handle, 3, sim.simx_opmode_blocking)
    cylinders = array(list(chunks(floatData, 3)))


    sim.simxGetPingTime(client_id)  # Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive.
    sim.simxFinish(client_id)  # Now close the connection to CoppeliaSim:
    print('Connection closed')

    print('Got obstacles')
    return (cuboids, cylinders)

def write_out(cuboids, cylinders):
    f = open("cuboids.txt", "w")
    f1 = open("cylinders.txt", "w")
    f.write(numpy.array2string(cuboids))
    f1.write(numpy.array2string(cylinders))
    f.close()
    f1.close()