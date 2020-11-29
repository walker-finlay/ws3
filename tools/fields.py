"""Convert coppeliasim obstacles to virtual potential fields \n
Walker Finlay"""

import numpy as np

def shapes2fields(cuboids, cylinders):
    # Cylinders: [x,y,z] -> [x,y,k]
    return

def cylinders2fields(cylinders, k=0.6):
    for cylinder in cylinders: cylinder[2] = k
    return cylinders

def cuboids2fields(cuboids, k=1.25):
    cuboids = np.delete(cuboids, np.s_[2:5], 1)
    # For now, just leave it as one big circle
    for cuboid in cuboids: cuboid[2] = k
    return cuboids