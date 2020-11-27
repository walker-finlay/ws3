import numpy as np

def shapes2fields(cuboids, cylinders):
    # Cylinders: [x,y,z] -> [x,y,k]
    return

def cylinders2fields(cylinders):
    for cylinder in cylinders: cylinder[2] = 0.6
    return cylinders

def cuboids2fields(cuboids):
    cuboids = np.delete(cuboids, np.s_[2:5], 1)
    # For now, just leave it as one big circle
    for cuboid in cuboids: cuboid[2] = 1.25
    return cuboids