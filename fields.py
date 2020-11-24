import sim
import sys
from math import floor, degrees, sin, cos
from numpy import array

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

# Plotem ----------------------------------------------------------------------
import matplotlib.pyplot as plt 
fig,ax = plt.subplots()
plt.grid(True)

for i in cylinders:
    ax.add_patch(plt.Circle(i, radius=0.5))
for i in cuboids:
    # coppelia gives us the center, pyplot wants the bottom left
    x = i[0]     # Initial position
    y = i[1]
    alpha = i[5] # Euler angles
    rotation = array([[cos(alpha), -sin(alpha)],
                    [sin(alpha), cos(alpha)]]) # Rotation
    pt = array([-2, -0.5]) # Bottom left of the rectangle
    new_pt = rotation.dot(pt) + array([x, y])
    ax.add_patch(plt.Rectangle(new_pt, 4, 1, degrees(alpha)))

plt.plot(7.625, 8.55, 'ro')     # Omnirob
plt.plot(-7.425, -7.925, 'go')  # Goal 

plt.xlim(-10,10)
plt.ylim(-10,10)
plt.gca().set_aspect("equal")
plt.show(block=True)